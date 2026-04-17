import pytest
from src.visitors.type_checker import *
from src.ast.nodes import *

def test_add():
    # OK test
    TypeCheckerVisitor().visit(Add(IntLiteral(2),IntLiteral(2)))
    TypeCheckerVisitor().visit(Add(FloatLiteral(2.0),FloatLiteral(2.0)))
    TypeCheckerVisitor().visit(Add(IntLiteral(2),FloatLiteral(2.0)))
    TypeCheckerVisitor().visit(Add(FloatLiteral(2.0),IntLiteral(2)))
    TypeCheckerVisitor().visit(Add(StringLiteral(2),StringLiteral(2)))
    
    # Error test
    with pytest.raises(TypeError):
        TypeCheckerVisitor().visit(Add(StringLiteral(2),IntLiteral(2)))

'''
------------------------
helper tests
------------------------

@pytest.mark.parametrize("value, expected", [
    (int, True),
    (float, True),
    (str, False),
    (bool, False),
])
def test_is_numeric(value, expected):
    assert is_numeric(value) is expected



------------------------
operator tests - valid
------------------------

# valid numeric operations
@pytest.mark.parametrize("x, op, y, expected", [
    (8, "+", 2, "OK -> int + int"),
    (8, "-", 2, "OK -> int - int"),
    (8, "+", 2.5, "OK -> int + float"),
    (2.1, "*", 3, "OK -> float * int"),
])
def test_check_op_valid_numeric(x, op, y, expected):
    assert check_op(x, op, y) == expected


# valid comparisons
@pytest.mark.parametrize("x, op, y, expected", [
    (8, "<", 2, "OK -> int < int"),
    (8.2, ">", 2, "OK -> float > int"),
    (8, "<", 2.2, "OK -> int < float"),
])
def test_check_op_valid_comparisons(x, op, y, expected):
    assert check_op(x, op, y) == expected


# valid string / bool / for-loop / between / chance operations
@pytest.mark.parametrize("x, op, y, expected", [
    ("hello", "+", "world", "OK -> str + str"),
    (True, "or", False, "OK -> bool or bool"),
    (True, "and", False, "OK -> bool and bool"),
    (True, "not", False, "OK -> bool not bool"),
    (1, "to", 10, "OK -> int to int"),
    (1, "between", 10, "OK -> int between int"),
    (1.5, "between", 10, "OK -> float between int"),
    (30, "chance", 100, "OK -> int chance int"),
    (25.0, "chance", 100, "OK -> float chance int"),
])
def test_check_op_valid_other(x, op, y, expected):
    assert check_op(x, op, y) == expected



------------------------
operator tests - invalid
------------------------

# mixed string with non-string
@pytest.mark.parametrize("x, op, y, expected", [
    ("hello", "+", 2, "TypeError: unsupported operand type(s) for +: 'str' and 'int'"),
    (2, "+", "hello", "TypeError: unsupported operand type(s) for +: 'int' and 'str'"),
    ("hello", "and", True, "TypeError: unsupported operand type(s) for and: 'str' and 'bool'"),
    (False, "+", "hello", "TypeError: unsupported operand type(s) for +: 'bool' and 'str'"),
])
def test_check_op_invalid_mixed_string(x, op, y, expected):
    assert check_op(x, op, y) == expected


# Addition: plus not allowed for bools
@pytest.mark.parametrize("x, op, y, expected", [
    (True, "+", 1, "TypeError: unsupported operand type(s) for +: 'bool' and 'int'"),
    (2, "+", False, "TypeError: unsupported operand type(s) for +: 'int' and 'bool'"),
    (True, "+", False, "TypeError: unsupported operand type(s) for +: 'bool' and 'bool'"),
])
def test_check_op_plus_bool_fails(x, op, y, expected):
    assert check_op(x, op, y) == expected


# Arithmetic: not allowed for bools
@pytest.mark.parametrize("x, op, y, expected", [
    (True, "-", 1, "TypeError: unsupported operand type(s) for -: 'bool' and 'int'"),
    (2.1, "*", False, "TypeError: unsupported operand type(s) for *: 'float' and 'bool'"),
    (1, "<", False, "TypeError: unsupported operand type(s) for <: 'int' and 'bool'"),
])
def test_check_op_arithmetic_bool_fails(x, op, y, expected):
    assert check_op(x, op, y) == expected


# Logical operators not allowed for non-bools
@pytest.mark.parametrize("x, op, y, expected", [
    (2, "or", False, "TypeError: unsupported operand type(s) for or: 'int' and 'bool'"),
    (2, "not", 2, "TypeError: unsupported operand type(s) for not: 'int' and 'int'"),
    (2.2, "and", 2, "TypeError: unsupported operand type(s) for and: 'float' and 'int'"),
])
def test_check_op_logical_invalid(x, op, y, expected):
    assert check_op(x, op, y) == expected


# 'to' should fail when both values are not int
@pytest.mark.parametrize("x, y, expected", [
    (2.5, 10, "TypeError: unsupported operand type(s) for to: 'float' and 'int'"),
    (10, 2.5, "TypeError: unsupported operand type(s) for to: 'int' and 'float'"),
    (True, 10, "TypeError: unsupported operand type(s) for to: 'bool' and 'int'"),
    (1, False, "TypeError: unsupported operand type(s) for to: 'int' and 'bool'"),
])
def test_check_op_to_invalid(x, y, expected):
    assert check_op(x, "to", y) == expected


# between / chance should fail for non-numerics
@pytest.mark.parametrize("x, op, y, expected", [
    ("hello", "between", 10, "TypeError: unsupported operand type(s) for between: 'str' and 'int'"),
    (1, "between", "hello", "TypeError: unsupported operand type(s) for between: 'int' and 'str'"),
    (True, "between", 10, "TypeError: unsupported operand type(s) for between: 'bool' and 'int'"),
    ("hello", "chance", 100, "TypeError: unsupported operand type(s) for chance: 'str' and 'int'"),
    (30, "chance", "hello", "TypeError: unsupported operand type(s) for chance: 'int' and 'str'"),
    (False, "chance", 100, "TypeError: unsupported operand type(s) for chance: 'bool' and 'int'"),
])
def test_check_op_between_chance_invalid(x, op, y, expected):
    assert check_op(x, op, y) == expected
'''