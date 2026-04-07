import pytest
from src.type_check import to_int, to_float, get_type, is_numeric, result_type, check_op


# ------------------------
# conversion tests
# ------------------------

# valid int conversion
@pytest.mark.parametrize("value, expected", [
    ("8", 8),
    ("-3", -3),
])
def test_to_int_valid(value, expected):
    assert to_int(value) == expected


# invalid int input
@pytest.mark.parametrize("value", [
    "hello",
    "2.5",
    "",
])
def test_to_int_invalid(value):
    assert to_int(value) is None


# valid float conversion
@pytest.mark.parametrize("value, expected", [
    ("2.5", 2.5),
    ("8", 8.0),
    ("-1.2", -1.2),
])
def test_to_float_valid(value, expected):
    assert to_float(value) == expected


# invalid float input
@pytest.mark.parametrize("value", [
    "hello",
    "",
])
def test_to_float_invalid(value):
    assert to_float(value) is None


# ------------------------
# type detection tests
# ------------------------

# basic type checks
@pytest.mark.parametrize("value, expected", [
    ("true", "bool"),
    ("false", "bool"),
    ("8", "int"),
    ("2.1", "float"),
    ("hello", "str"),
])
def test_get_type(value, expected):
    assert get_type(value) == expected


# some extra type cases
@pytest.mark.parametrize("value, expected", [
    ("-5", "int"),
    ("-2.3", "float"),
    ("", "str"),
    ("   ", "str"),
    ("True", "str"),
    ("False", "str"),
])
def test_get_type_edge_cases(value, expected):
    assert get_type(value) == expected

#zero values (fails)
@pytest.mark.xfail(reason="0 case currently fails")
@pytest.mark.parametrize("value, expected", [
    ("0", "int"),
    ("0.0", "float"),
])
def test_get_type_zero_cases(value, expected):
    assert get_type(value) == expected

# ------------------------
# helper function tests
# ------------------------

# numeric type check
@pytest.mark.parametrize("value, expected", [
    ("int", True),
    ("float", True),
    ("str", False),
    ("bool", False),
])
def test_is_numeric(value, expected):
    assert is_numeric(value) is expected


# result type for numeric operations
@pytest.mark.parametrize("t1, t2, expected", [
    ("int", "int", "int"),
    ("int", "float", "float"),
    ("float", "int", "float"),
    ("float", "float", "float"),
])
def test_result_type(t1, t2, expected):
    assert result_type(t1, t2) == expected


# ------------------------
# operator tests - valid
# ------------------------

# valid numeric operations
@pytest.mark.parametrize("x, op, y, expected", [
    ("8", "+", "2", "OK -> int"),
    ("8", "-", "2", "OK -> int"),
    ("8", "/", "2", "OK -> int"),
    ("8", "*", "2.1", "OK -> float"),
    ("2.1", "*", "3", "OK -> float"),
    ("8", "+", "2.5", "OK -> float"),
])
def test_check_op_valid_numeric(x, op, y, expected):
    assert check_op(x, op, y) == expected


# valid comparisons
@pytest.mark.parametrize("x, op, y", [
    ("8", "<", "2"),
    ("8", ">", "2"),
    ("8", "<=", "2"),
    ("8", ">=", "2"),
    ("8", "==", "2"),
    ("8", "!=", "2"),
])
def test_check_op_valid_comparisons(x, op, y):
    assert check_op(x, op, y) == "OK -> bool"


# valid string / bool operations
@pytest.mark.parametrize("x, op, y, expected", [
    ("hello", "+", " world", "OK -> '+' string"),
    ("true", "or", "false", "OK -> bool"),
    ("true", "and", "false", "OK -> bool"),
    ("true", "not", "false", "OK -> bool"),
])
def test_check_op_valid_non_numeric(x, op, y, expected):
    assert check_op(x, op, y) == expected


# ------------------------
# operator tests - invalid
# ------------------------

# invalid operations / type errors
@pytest.mark.parametrize("x, op, y, expected", [
    ("hello", "+", "2", "TypeError: str '+' int not allowed"),
    ("false", "+", "Hello", "TypeError: bool '+' str not allowed"),
    ("9", "+", "Hello", "TypeError: int '+' str not allowed"),
    ("8", "*", "true", "TypeError: '*' not allowed for int"),
    ("false", "*", "true", "TypeError: '*' not allowed for bool"),
    ("hello", "<", "world", "TypeError: '<' not allowed for str"),
    ("true", "and", "2", "TypeError: 'and' not allowed for bool"),
    ("8", "%", "2", "Unknown operator"),
    ("8", "???", "2", "Unknown operator"),
])
def test_check_op_invalid_cases(x, op, y, expected):
    assert check_op(x, op, y) == expected


# same-type bools with + should fail
def test_check_op_plus_bool_bool_fails():
    assert check_op("true", "+", "false") == "TypeError: '+' not allowed for bool"


# mixed float/string and str/bool cases
@pytest.mark.parametrize("x, op, y, expected", [
    ("2.5", "+", "hello", "TypeError: float '+' str not allowed"),
    ("hello", "and", "true", "TypeError: str 'and' bool not allowed"),
])
def test_check_op_mixed_string_cases(x, op, y, expected):
    assert check_op(x, op, y) == expected


# bools with arithmetic ops that are not already covered
@pytest.mark.parametrize("op", ["-", "/"])
def test_check_op_arithmetic_bool_bool_fails(op):
    assert check_op("true", op, "false") == f"TypeError: '{op}' not allowed for bool"


# bools with comparison ops
@pytest.mark.parametrize("op", ["<", ">", "<=", ">=", "==", "!="])
def test_check_op_comparison_bool_bool_fails(op):
    assert check_op("true", op, "false") == f"TypeError: '{op}' not allowed for bool"


# ints with logical ops should fail
@pytest.mark.parametrize("op", ["and", "or", "not"])
def test_check_op_logical_int_int_fails(op):
    assert check_op("8", op, "2") == f"TypeError: '{op}' not allowed for int"


# ------------------------
# extra helper edge cases
# ------------------------

# non-numeric names should stay false
@pytest.mark.parametrize("value, expected", [
    ("g", False),
    ("   ", False),
    ("boolean", False),
    ("", False),
])
def test_is_numeric_edge_cases(value, expected):
    assert is_numeric(value) is expected