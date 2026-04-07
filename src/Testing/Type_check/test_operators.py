import pytest
from src.type_check import get_type, is_numeric, check_op

'''
------------------------
type detection tests
------------------------
'''
# basic type checks
@pytest.mark.parametrize("value, expected", [
    ("true", bool),
    ("false", bool),
    ("8", int),
    ("0", int),
    ("2.1", float),
    ("0.0", float),
    ("hello", str),
])
def test_get_type(value, expected):
    assert get_type(value) is expected


# extra type cases
@pytest.mark.parametrize("value, expected", [
    ("-5", int),
    ("-2.3", float),
    ("", str),
    ("   ", str),
    ("True", str),
    ("False", str),
])
def test_get_type_edge_cases(value, expected):
    assert get_type(value) is expected

'''
------------------------
helper tests
------------------------
'''
# numeric type check
@pytest.mark.parametrize("value, expected", [
    (int, True),
    (float, True),
    (str, False),
    (bool, False),
])
def test_is_numeric(value, expected):
    assert is_numeric(value) is expected

'''
------------------------
operator tests - valid
------------------------
'''
# valid numeric operations
@pytest.mark.parametrize("x, op, y, expected", [
    ("8", "+", "2", "OK -> int + int"),
    ("8", "-", "2", "OK -> int - int"),
    ("8", "+", "2.5", "OK -> int + float"),
    ("2.1", "*", "3", "OK -> float * int"),
])
def test_check_op_valid_numeric(x, op, y, expected):
    assert check_op(x, op, y) == expected


# valid comparisons
@pytest.mark.parametrize("x, op, y, expected", [
    ("8", "<", "2", "OK -> int < int"),
    ("8.2", ">", "2", "OK -> float > int"),
    ("8", "<", "2.2", "OK -> int < float"),
])
def test_check_op_valid_comparisons(x, op, y, expected):
    assert check_op(x, op, y) == expected


# valid string / bool / for-loop operations
@pytest.mark.parametrize("x, op, y, expected", [
    ("hello", "+", "world", "OK -> str + str"),
    ("true", "or", "false", "OK -> bool or bool"),
    ("true", "and", "false", "OK -> bool and bool"),
    ("true", "not", "false", "OK -> bool not bool"),
    ("1", "to", "10", "OK -> int to int"),
])
def test_check_op_valid_other(x, op, y, expected):
    assert check_op(x, op, y) == expected

'''
------------------------
operator tests - invalid
------------------------
'''
# mixed string with non-string
@pytest.mark.parametrize("x, op, y, expected", [
    ("hello", "+", "2", "TypeError: unsupported operand type(s) for +: 'str' and 'int'"),
    ("2", "+", "hello", "TypeError: unsupported operand type(s) for +: 'int' and 'str'"),
    ("hello", "and", "true", "TypeError: unsupported operand type(s) for and: 'str' and 'bool'"),
    ("false", "+", "hello", "TypeError: unsupported operand type(s) for +: 'bool' and 'str'"),
])
def test_check_op_invalid_mixed_string(x, op, y, expected):
    assert check_op(x, op, y)


# Addition: plus not allowed for bools
@pytest.mark.parametrize("x, op, y, expected", [
    ("true", "+", "1", "TypeError: unsupported operand type(s) for +: 'bool' and 'int'"),
    ("2", "+", "false", "TypeError: unsupported operand type(s) for +: 'int' and bool'"),
    ("true", "+", "false", "TypeError: unsupported operand type(s) for +: 'float' and 'bool'"),
])
def test_check_op_plus_bool_bool_fails(x, op, y, expected):
    assert check_op(x, op, y)

# Arithmetic: not allowed for bools
@pytest.mark.parametrize("x, op, y, expected", [
    ("true", "-", "1", "TypeError: unsupported operand type(s) for -: 'bool' and 'int'"),
    ("2.1", "*", "false", "TypeError: unsupported operand type(s) for *: 'float' and bool'"),
    ("1", "<", "false", "TypeError: unsupported operand type(s) for <: 'int' and 'bool'"),
])
def test_check_op_arithmetic_bool_bool_fails(x, op, y, expected):
    assert check_op(x, op, y)

# Logical operators not allowed, for bool and mix of bool
@pytest.mark.parametrize("x, op, y, expected", [
    ("2", "or", "false", "TypeError: unsupported operand type(s) for or: 'int' and 'bool'"),
    ("2", "not", "2", "TypeError: unsupported operand type(s) for not: 'int' and int'"),
    ("2.2", "and", "2", "TypeError: unsupported operand type(s) for and: 'float' and 'int'"),
])
def test_check_op_logical_int_int_fails(x, op, y, expected):
    assert check_op(x, op, y)

# 'to' should fail when both values is not int
@pytest.mark.parametrize("x, y, expected", [
    ("2.5", "10", "TypeError: unsupported operand type(s) for to: 'float' and 'int'"),
    ("10", "2.5", "TypeError: unsupported operand type(s) for to: 'int' and 'float'"),
    ("true", "10", "TypeError: unsupported operand type(s) for to: 'bool' and 'int'"),
    ("1", "false", "TypeError: unsupported operand type(s) for to: 'int' and 'bool'"),
])
def test_check_op_to_invalid_left_side(x, y, expected):
    assert check_op(x, "to", y) == expected