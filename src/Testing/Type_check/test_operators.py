import pytest
from src.type_check import get_type, is_numeric, check_op


# ------------------------
# type detection tests
# ------------------------

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


# ------------------------
# helper tests
# ------------------------

# numeric type check
@pytest.mark.parametrize("value, expected", [
    (int, True),
    (float, True),
    (str, False),
    (bool, False),
])
def test_is_numeric(value, expected):
    assert is_numeric(value) is expected


# ------------------------
# operator tests - valid
# ------------------------

# valid numeric operations
@pytest.mark.parametrize("x, op, y, expected", [
    ("8", "+", "2", "OK -> int + int"),
    ("8", "-", "2", "OK -> int - int"),
    ("8", "*", "2", "OK -> int * int"),
    ("8", "/", "2", "OK -> int / int"),
    ("8", "+", "2.5", "OK -> int + float"),
    ("2.1", "*", "3", "OK -> float * int"),
])
def test_check_op_valid_numeric(x, op, y, expected):
    assert check_op(x, op, y) == expected


# valid comparisons
@pytest.mark.parametrize("x, op, y, expected", [
    ("8", "<", "2", "OK -> int < int"),
    ("8", ">", "2", "OK -> int > int"),
    ("8", "<=", "2", "OK -> int <= int"),
    ("8", ">=", "2", "OK -> int >= int"),
    ("8", "==", "2", "OK -> int == int"),
    ("8", "!=", "2", "OK -> int != int"),
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


# ------------------------
# operator tests - invalid
# ------------------------

# mixed string with non-string
@pytest.mark.parametrize("x, op, y, expected", [
    ("hello", "+", "2", "TypeError: unsupported operand type(s) for +: 'str' and 'int'"),
    ("2", "+", "hello", "TypeError: unsupported operand type(s) for +: 'int' and 'str'"),
    ("hello", "and", "true", "TypeError: unsupported operand type(s) for and: 'str' and 'bool'"),
    ("false", "+", "hello", "TypeError: unsupported operand type(s) for +: 'bool' and 'str'"),
])
def test_check_op_invalid_mixed_string(x, op, y, expected):
    assert check_op(x, op, y)


# plus not allowed for bools
def test_check_op_plus_bool_bool_fails():
    assert check_op("true", "+", "false") == \
        "TypeError: unsupported operand type(s) for +: 'bool' and 'bool'"


# arithmetic not allowed for bools
@pytest.mark.parametrize("op", ["-", "*", "/"])
def test_check_op_arithmetic_bool_bool_fails(op):
    assert check_op("true", op, "false") == \
        f"TypeError: unsupported operand type(s) for {op}: 'bool' and 'bool'"


# comparison not allowed for bools in current implementation
@pytest.mark.parametrize("op", ["<", ">", "<=", ">=", "==", "!="])
def test_check_op_comparison_bool_bool_fails(op):
    assert check_op("true", op, "false") == \
        f"TypeError: unsupported operand type(s) for {op}: 'bool' and 'bool'"


# logical operators not allowed for ints
@pytest.mark.parametrize("op", ["and", "or", "not"])
def test_check_op_logical_int_int_fails(op):
    assert check_op("8", op, "2") == \
        f"TypeError: unsupported operand type(s) for {op}: 'int' and 'int'"


# 'to' should fail when left side is not int
@pytest.mark.parametrize("x, y, expected", [
    ("2.5", "10", "TypeError: unsupported operand type(s) for to: 'float' and 'int'"),
    ("true", "10", "TypeError: unsupported operand type(s) for to: 'bool' and 'int'"),
    ("hello", "10", "TypeError: unsupported operand type(s) for to: 'str' and 'int'"),
])
def test_check_op_to_invalid_left_side(x, y, expected):
    assert check_op(x, "to", y) == expected