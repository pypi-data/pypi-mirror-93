from typing import List, ClassVar, Callable
import re

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor, Node

from .base_types import Expression, BooleanOperation, BinaryOperation, Field


class EncoderVisitor(NodeVisitor):

    def visit_field(self, node: Node, visited_children: List) -> Field:
        return Field(name=node.text)

    # def visit_number(self, node: Node, visited_children: List):
    #     return float(node.text)
    #
    # def visit_true(self, node: Node, visited_children: List) -> bool:
    #     return True
    #
    # def visit_false(self, node: Node, visited_children: List) -> bool:
    #     return False
    #
    # def visit_string(self, node: Node, visited_children: List) -> bool:
    #     matches = re.findall(r"^'(.*)'$", node.text)
    #     if len(matches) != 1:
    #         raise AssertionError(f'Expected regular expression of string to have one '
    #                              f'match (found {len(matches)} matches), probably string '
    #                              f'has an invalid format')
    #     value = matches[0]
    #     return value

    def visit_expression(self, node: Node, visited_children: List) -> Expression:
        # Ignore children that do not have an encoding
        # result (mostly spaces & symbols not needed in the resulting expression)
        _visited_children = [c for c in visited_children if c]
        _visited_children = _visited_children[0] if len(_visited_children) == 1 else _visited_children

        # The expression is always in the format: a operator b
        operator = _visited_children[1]
        a = _visited_children[0]
        b = _visited_children[2]

        if issubclass(operator, BooleanOperation):
            return operator(operands=[a, b])
        elif issubclass(operator, BinaryOperation):
            return operator(field=a, value=b)

        raise Exception(f'Unknown expression type. operator: {operator}')

    def generic_visit(self, node: Node, visited_children: List) -> List:

        # Basically pass the values from the children forward & ignore children with no encoding
        _visited_children = [c for c in visited_children if c]
        return _visited_children[0] if len(_visited_children) == 1 else _visited_children


class Encoder:
    """
    This encoder enables you to encode a filtering string into a structured expression.
    """

    _base_peg_grammar = r"""
    expression = "(" nspaces 
                     ( 
                         (field spaces ratio spaces value) /
                         (expression spaces binary_logical_operator spaces expression) 
                     ) 
                 nspaces ")" 

    # # Values
    # string = "'" ~"[^']*"i "'"
    # # TODO: Write a smarter num regex to accept decimals & ignore -0, 00019
    # number = ~"-?\d+"i
    # true = "true"
    # false = "false"
    # boolean = true / false
    # value = string / number / boolean

    # Spaces
    spaces = " "+
    nspaces = spaces?

    # Fields
    field = key ("\\" key)*
    key = ~"[a-z]([a-z]|[0-9]|_)*"i&(" ")
    # key = "age"

    # Auto generated rules come here
    """

    def __init__(self):
        # A map of ratio symbols to a BinaryOperation class
        self.registered_ratios = {}

        # A map of binary logical operator symbols to a BooleanOperation class
        self.registered_binary_logical_operators = {}

        self.registered_types = {}

        # An object that traverses the raw expression tree and recursively transforms it to a Expression object
        self._encoder_visitor = EncoderVisitor()

    def register_ratio(self, symbol: str):
        """
        Register a new type of ratio into the encoder.
        once the new ratio is registered, the encoder is able to detect that new ratio.

        The class being decorated must be a subclass of the BinaryOperation class
        :param symbol: The symbol that represents this ratio in the unencoded expression
        :return: A decorator for a ratio class
        """

        # When registering a new ratio we do two things:
        # 1. Add a rule for the new ratio to the PEG grammar. this is done
        #    by saving the ratio the the ratios dictionary that stored the ratios class & symbol
        # 2. Add a "visit__*" function to the encoder visitor object, so the encoder visitor
        #    can handle "visiting" a rule of this type
        def register_decorator(cls: ClassVar):
            grammar_rule_name = f'registered_ratio_{cls.__name__}'
            self.registered_ratios[grammar_rule_name] = {
                'class': cls,
                'symbol': symbol
            }

            # Create the visitor func that returns the ratio class
            visit_func_name = f'visit_{grammar_rule_name}'
            setattr(self._encoder_visitor, visit_func_name, lambda *args, **kwargs: cls)

            return cls

        return register_decorator

    def register_binary_logical_operator(self, symbol: str):
        """
        Register a new type of binary logical operator into the encoder.
        once the new operator is registered, the encoder is able to detect that new operator

        A binary logical operator is an operator that accepts two
        logical values / expressions representing boolean values and returns a single boolean value.

        The class being decorated must be a subclass of the BinaryOperation class
        :param symbol: The symbol that represents this operation in the unencoded expression
        :return: A decorator for a binary boolean operator class
        """

        # When registering a new logical operator we do two things:
        # 1. Add a rule for the new operator to the PEG grammar. this is done
        #    by saving the operator the the logical operators dictionary that stored
        #    the operators class & symbol
        # 2. Add a "visit__*" function to the encoder visitor object, so the encoder visitor
        #    can handle "visiting" a rule of this type
        def register_decorator(cls: ClassVar):
            grammar_rule_name = f'registered_binary_logical_operator_{cls.__name__}'
            self.registered_binary_logical_operators[grammar_rule_name] = {
                'class': cls,
                'symbol': symbol
            }

            # Create the visitor func that returns the operator class
            visit_func_name = f'visit_{grammar_rule_name}'
            setattr(self._encoder_visitor, visit_func_name, lambda *args, **kwargs: cls)

            return cls

        return register_decorator

    def register_type(self, regular_expression: str):
        """
        Register a type of a value. The decorated function is called with them matching
        text and should return the parsed value (i.e. string, number, bool...)

        :param regular_expression: A regular expression matching values of this type
        :return: A function decotator
        """

        def register_decorator(f: Callable):
            grammar_rule_name = f'registered_type_{f.__name__}'
            self.registered_types[grammar_rule_name] = {
                'regular_expression': regular_expression
            }

            # Create the visitor func that parsed & returns the value
            visit_func_name = f'visit_{grammar_rule_name}'
            setattr(self._encoder_visitor, visit_func_name, lambda node, *args, **kwargs: f(node.text))

            return f

        return register_decorator

    def _get_peg_format_grammar(self) -> str:
        """
        Generate and return the PEG grammar of the encoder
        :return: A multiline string of the encoders PEG grammar, including the registered objects
        """

        lines = self._base_peg_grammar.splitlines()

        # Add ratios to grammar
        lines.append('')
        lines.append('# Ratio rules')
        ratios_rule = f'ratio = {" / ".join(self.registered_ratios.keys())}'
        lines.append(ratios_rule)
        for rule_name, data in self.registered_ratios.items():
            lines.append(f'{rule_name} = "{data["symbol"]}"')

        # Add binary logical operators to grammar
        lines.append('')
        lines.append('# Binary logical operators rules')
        binary_boolean_operations_rule = f'binary_logical_operator = ' \
            f'{" / ".join(self.registered_binary_logical_operators.keys())}'
        lines.append(binary_boolean_operations_rule)
        for rule_name, data in self.registered_binary_logical_operators.items():
            lines.append(f'{rule_name} = "{data["symbol"]}"')

        # Add value types to grammar
        lines.append('')
        lines.append('# Value types rules')
        for rule_name, data in self.registered_types.items():
            regular_expression = data["regular_expression"].replace('"', '\\"')
            lines.append(f'{rule_name} = ~"{regular_expression}"i')
        lines.append('')
        lines.append(f'value = '
                     f'{" / ".join([type_rule for type_rule in self.registered_types.keys()])}')

        final_grammar = '\n'.join(lines)

        return final_grammar

    def encode_expression(self, expression: str) -> Expression:
        """
        Encode an unencoded expression into an Expression object representing the input
        :param expression: a string representing a boolean expression
        :return: an Expression representing the given expression string
        """

        grammar = Grammar(self._get_peg_format_grammar())
        expression_tree = grammar.parse(expression)
        encoded_expression: Expression = self._encoder_visitor.visit(expression_tree)

        return encoded_expression
