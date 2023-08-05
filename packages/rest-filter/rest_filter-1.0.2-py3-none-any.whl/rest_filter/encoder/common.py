import re

from .encoder import Encoder
from .base_types import BooleanOperation, BinaryOperation

# This is an encoder "pre loaded" with common logical operators & ratios.
# Basically a "Good enough to start with" encoder
encoder = Encoder()


@encoder.register_binary_logical_operator('and')
class And(BooleanOperation):
    pass


@encoder.register_binary_logical_operator('or')
class Or(BooleanOperation):
    pass


@encoder.register_ratio('gt')
class GraterThan(BinaryOperation):
    pass


@encoder.register_ratio('ge')
class GraterEqualsTo(BinaryOperation):
    pass


@encoder.register_ratio('lt')
class LessThan(BinaryOperation):
    pass


@encoder.register_ratio('le')
class LessEqualsTo(BinaryOperation):
    pass


@encoder.register_ratio('eq')
class Equals(BinaryOperation):
    pass


@encoder.register_ratio('ne')
class NotEquals(BinaryOperation):
    pass


@encoder.register_type(r'-?\d+')
def number(text: str):
    return int(text)


@encoder.register_type("(('[^']*')|\"[^\"]*\")")
def text(text: str):
    return text[1:-1]


@encoder.register_type(r"(true|false)")
def boolean(text: str):
    return text.lower() == 'true'


@encoder.register_type(r'-?\d+(kb|mb|gb|tb)')
def number(text: str):
    matches = re.findall(r'(-?\d+)(kb|mb|gb|tb)', text)
    value, unit = int(matches[0][0]), matches[0][1]

    if unit == 'kb':
        return value * 1024
    elif unit == 'mb':
        return value * 1024 * 1024
    elif unit == 'gb':
        return value * 1024 * 1024 * 1024
    elif unit == 'tb':
        return value * 1024 * 1024 * 1024 * 1024

    raise Exception(f'Unknown unit: {unit}')
