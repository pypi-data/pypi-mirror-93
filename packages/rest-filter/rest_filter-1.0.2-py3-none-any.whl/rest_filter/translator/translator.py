from typing import List, Dict, Any

from rest_filter.encoder import Expression, BinaryOperation, BooleanOperation


class Translator:

    def __init__(self):
        self.binary_operation_translators: List[Dict] = []
        self.boolean_operation_translators: List[Dict] = []

    def translate(self, encoded_expression: Expression) -> Any:
        """
        Translates an expression into the target language
        :param encoded_expression: The boolean expression to translate
        :return: The input expression in the target language
        """

        if isinstance(encoded_expression, BinaryOperation):

            # Check that list of registered binary operations to find one
            # that matches to the expression. if found, translate using the match
            for translator_info in self.binary_operation_translators:
                cls = translator_info['class']
                translator = translator_info['translator']

                if isinstance(encoded_expression, cls):
                    return translator(encoded_expression)

            raise Exception(f'Unknown binary operation type: {type(encoded_expression)}')

        elif isinstance(encoded_expression, BooleanOperation):

            # Check that list of registered boolean operations to find one
            # that matches to the expression. if found, translate using the match
            for translator_info in self.boolean_operation_translators:
                cls = translator_info['class']
                translator = translator_info['translator']

                if isinstance(encoded_expression, cls):
                    return translator(encoded_expression, self)

            raise Exception(f'Unknown boolean operation type: {type(encoded_expression)}')

        raise Exception(f'Unknown expression type: {type(encoded_expression)}')

    def register_binary_operation_translator(self, binary_operation: BinaryOperation):
        """
        Register a translation function from encoded form into target language
        :param binary_operation: The encoded binary operation type that matches this translation
        :return: A decorator for the translation function
        """

        def decorator(func):

            # Make sure that the given class isn't registered as a translator already
            for translator_info in self.binary_operation_translators:
                cls = translator_info['class']
                if issubclass(binary_operation, cls):
                    raise Exception(f'The translator class {binary_operation} superseded '
                                    f'by existing translator class {cls}')

            self.binary_operation_translators.append({
                'class': binary_operation,
                'translator': func
            })

            return func

        return decorator

    def register_boolean_operation_translator(self, boolean_operation: BooleanOperation):
        """
        Register a translation function from encoded form into target language
        :param boolean_operation: The encoded boolean operation type that matches this translation
        :return: A decorator for the translation function
        """

        def decorator(func):

            # Make sure that the given class isn't registered as a translator already
            for translator_info in self.boolean_operation_translators:
                cls = translator_info['class']
                if issubclass(boolean_operation, cls):
                    raise Exception(f'The translator class {boolean_operation} superseded '
                                    f'by existing translator class {cls}')

            self.boolean_operation_translators.append({
                'class': boolean_operation,
                'translator': func
            })

            return func

        return decorator
