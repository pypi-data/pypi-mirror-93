from rest_filter.encoder.common import (
    And, Or,
    GraterThan, GraterEqualsTo, LessThan, LessEqualsTo,
    Equals, NotEquals
)
from .translator import Translator


def get_mssql_translator() -> Translator:
    """
    Returns an microsoft sql translator for the common encoder
    :return: A translator for microsoft sql language
    """
    mssql_translator = Translator()

    # Register boolean logical operators
    @mssql_translator.register_boolean_operation_translator(And)
    def translate_and(operation: And, translator: Translator):
        condition = ' AND '.join([
            translator.translate(operand) for operand in operation.operands
        ])
        condition = f'({condition})'

        return condition

    @mssql_translator.register_boolean_operation_translator(Or)
    def translate_or(operation: Or, translator: Translator):
        condition = ' OR '.join([
            translator.translate(operand) for operand in operation.operands
        ])
        condition = f'({condition})'

        return condition

    # Register ratios

    @mssql_translator.register_binary_operation_translator(Equals)
    def translate_equals(operation: Equals):
        if isinstance(operation.value, int):
            return f'({operation.field.name} = {operation.value})'
        elif isinstance(operation.value, str):
            return f"({operation.field.name} = '{operation.value})'"

        raise Exception(f'Unsupported value type: {type(operation.value)}')

    @mssql_translator.register_binary_operation_translator(NotEquals)
    def translate_not_equals(operation: NotEquals):
        if isinstance(operation.value, int):
            return f'({operation.field.name} <> {operation.value})'
        elif isinstance(operation.value, str):
            return f"({operation.field.name} <> '{operation.value})'"

        raise Exception(f'Unsupported value type: {type(operation.value)}')

    @mssql_translator.register_binary_operation_translator(GraterThan)
    def translate_grater_than(operation: GraterThan):
        if isinstance(operation.value, int):
            return f'({operation.field.name} > {operation.value})'

        raise Exception(f'Unsupported value type: {type(operation.value)}')

    @mssql_translator.register_binary_operation_translator(GraterEqualsTo)
    def translate_grater_equals_to(operation: GraterEqualsTo):
        if isinstance(operation.value, int):
            return f'({operation.field.name} >= {operation.value})'

        raise Exception(f'Unsupported value type: {type(operation.value)}')

    @mssql_translator.register_binary_operation_translator(LessThan)
    def translate_less_than(operation: LessThan):
        if isinstance(operation.value, int):
            return f'({operation.field.name} < {operation.value})'

        raise Exception(f'Unsupported value type: {type(operation.value)}')

    @mssql_translator.register_binary_operation_translator(LessEqualsTo)
    def translate_less_equals_to(operation: LessEqualsTo):
        if isinstance(operation.value, int):
            return f'({operation.field.name} <= {operation.value})'

        raise Exception(f'Unsupported value type: {type(operation.value)}')

    return mssql_translator
