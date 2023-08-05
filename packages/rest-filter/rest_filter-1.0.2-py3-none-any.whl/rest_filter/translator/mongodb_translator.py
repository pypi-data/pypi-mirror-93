from rest_filter.encoder.common import (
    And, Or,
    GraterThan, GraterEqualsTo, LessThan, LessEqualsTo,
    Equals, NotEquals
)
from .translator import Translator


def get_mongo_translator() -> Translator:
    """
    Returns a mongo translator for the common encoder
    :return: A translator for mongodb filters
    """
    mongo_translator = Translator()

    # Register boolean logical operators
    @mongo_translator.register_boolean_operation_translator(And)
    def translate_and(operation: And, translator: Translator):
        return {
            '$and': [
                translator.translate(operand) for operand in operation.operands
            ]
        }

    @mongo_translator.register_boolean_operation_translator(Or)
    def translate_or(operation: Or, translator: Translator):
        return {
            '$or': [
                translator.translate(operand) for operand in operation.operands
            ]
        }

    # Register ratios

    @mongo_translator.register_binary_operation_translator(Equals)
    def translate_equals(operation: Equals):
        return {
            operation.field.name: {
                '$eq': operation.value
            }
        }

    @mongo_translator.register_binary_operation_translator(NotEquals)
    def translate_not_equals(operation: NotEquals):
        return {
            operation.field.name: {
                '$ne': operation.value
            }
        }

    @mongo_translator.register_binary_operation_translator(GraterThan)
    def translate_grater_than(operation: GraterThan):
        return {
            operation.field.name: {
                '$gt': operation.value
            }
        }

    @mongo_translator.register_binary_operation_translator(GraterEqualsTo)
    def translate_grater_than(operation: GraterEqualsTo):
        return {
            operation.field.name: {
                '$ge': operation.value
            }
        }

    @mongo_translator.register_binary_operation_translator(LessThan)
    def translate_less_than(operation: LessThan):
        return {
            operation.field.name: {
                '$lt': operation.value
            }
        }

    @mongo_translator.register_binary_operation_translator(LessEqualsTo)
    def translate_less_than(operation: LessEqualsTo):
        return {
            operation.field.name: {
                '$le': operation.value
            }
        }

    return mongo_translator
