import pytest
from src.visitors.type_checker import *
from src.ast.nodes import *

def make_checker():
    return TypeCheckerVisitor()

# -------------------------
# basic helpers / literals
# -------------------------

def test_is_numeric():
    checker = make_checker()
    assert checker.is_numeric("int") is True
    assert checker.is_numeric("float") is True
    assert checker.is_numeric("str") is False
    assert checker.is_numeric("bool") is False
    assert checker.is_numeric(None) is False


def test_numeric_result_type():
    checker = make_checker()

    assert checker.numeric_result_type(None, "int", "int") == "int"
    assert checker.numeric_result_type(None, "int", "float") == "float"
    assert checker.numeric_result_type(None, "float", "int") == "float"
    assert checker.numeric_result_type(None, "float", "float") == "float"

    with pytest.raises(TypeError, match="Expected numeric types"):
        checker.numeric_result_type(None, "str", "int")


def test_literal_visits():
    checker = make_checker()

    assert checker.visit(IntLiteral(2)) == "int"
    assert checker.visit(FloatLiteral(2.5)) == "float"
    assert checker.visit(StringLiteral("hello")) == "str"
    assert checker.visit(BoolLiteral(True)) == "bool"

# -------------------------
# arithmetic
# -------------------------

def test_add():
    checker = make_checker()

    assert checker.visit(Add(IntLiteral(2), IntLiteral(2))) == "int"
    assert checker.visit(Add(FloatLiteral(2.0), FloatLiteral(2.0))) == "float"
    assert checker.visit(Add(IntLiteral(2), FloatLiteral(2.0))) == "float"
    assert checker.visit(Add(FloatLiteral(2.0), IntLiteral(2))) == "float"
    assert checker.visit(Add(StringLiteral("a"), StringLiteral("b"))) == "str"

    with pytest.raises(TypeError, match="Expected numeric types"):
        checker.visit(Add(StringLiteral("a"), IntLiteral(2)))


# we need to take another look at "-"

def test_mul():
    checker = make_checker()

    assert checker.visit(Mul(IntLiteral(2), IntLiteral(2))) == "int"
    assert checker.visit(Mul(IntLiteral(2), FloatLiteral(2.0))) == "float"

    with pytest.raises(TypeError, match="Expected numeric types"):
        checker.visit(Mul(StringLiteral("a"), IntLiteral(2)))


def test_div():
    checker = make_checker()

    assert checker.visit(Div(IntLiteral(4), IntLiteral(2))) == "float"
    assert checker.visit(Div(FloatLiteral(4.0), IntLiteral(2))) == "float"

    with pytest.raises(TypeError, match="Expected numeric types"):
        checker.visit(Div(StringLiteral("a"), IntLiteral(2)))


def test_pow():
    checker = make_checker()

    assert checker.visit(Pow(IntLiteral(2), IntLiteral(3))) == "int"
    assert checker.visit(Pow(IntLiteral(2), FloatLiteral(3.0))) == "float"

    with pytest.raises(TypeError, match="Expected numeric types"):
        checker.visit(Pow(StringLiteral("a"), IntLiteral(2)))

# -------------------------
# variables
# -------------------------

def test_create_variable():
    checker = make_checker()

    assert checker.visit(CreateVariable("x", IntLiteral(5))) == "int"
    assert checker.v_table["x"] == "int"


def test_create_variable_without_value():
    checker = make_checker()

    assert checker.visit(CreateVariable("x", None)) is None
    assert "x" in checker.v_table
    assert checker.v_table["x"] is None


def test_create_variable_duplicate_fails():
    checker = make_checker()
    checker.visit(CreateVariable("x", IntLiteral(5)))

    with pytest.raises(TypeError, match="already exist"):
        checker.visit(CreateVariable("x", IntLiteral(10)))


def test_visit_var_existing_variable():
    checker = make_checker()
    checker.v_table["x"] = "int"

    assert checker.visit(Var("x", None)) == "int"


def test_visit_var_missing_variable_fails():
    checker = make_checker()

    with pytest.raises(TypeError, match="don't exist"):
        checker.visit(Var("x", None))


def test_assign_existing_variable():
    checker = make_checker()
    checker.v_table["x"] = "int"

    assert checker.visit(Assign("x", None, IntLiteral(10))) == "int"
    assert checker.v_table["x"] == "int"


def test_assign_missing_variable_fails():
    checker = make_checker()

    with pytest.raises(TypeError, match="don't exist"):
        checker.visit(Assign("x", None, IntLiteral(10)))

def test_assign_existing_variable_can_change_type_current_behavior():
    checker = make_checker()
    checker.v_table["x"] = "int"

    result = checker.visit(Assign("x", None, StringLiteral("hello")))

    assert result == "str"
    assert checker.v_table["x"] == "str"


def test_assign_list_variable_can_change_type_current_behavior():
    checker = make_checker()
    checker.v_table["xs"] = "list[int]"

    result = checker.visit(Assign("xs", None, StringLiteral("hello")))

    assert result == "str"
    assert checker.v_table["xs"] == "str"

# -------------------------
# comparisons
# -------------------------

def test_comparable_helpers():
    checker = make_checker()

    assert checker.comparable_ordered("int", "float") is True
    assert checker.comparable_ordered("int", "str") is False

    assert checker.comparable_equality("int", "int") is True
    assert checker.comparable_equality("int", "float") is True
    assert checker.comparable_equality("str", "str") is True
    assert checker.comparable_equality("str", "bool") is False


def test_equal_expr():
    checker = make_checker()

    assert checker.visit(EqualExpr(IntLiteral(1), IntLiteral(1))) == "bool"
    assert checker.visit(EqualExpr(IntLiteral(1), FloatLiteral(1.0))) == "bool"
    assert checker.visit(EqualExpr(StringLiteral("a"), StringLiteral("b"))) == "bool"

    with pytest.raises(TypeError, match="Cannot compare"):
        checker.visit(EqualExpr(StringLiteral("a"), IntLiteral(1)))


def test_not_equal_expr():
    checker = make_checker()

    assert checker.visit(NotEqualExpr(IntLiteral(1), FloatLiteral(1.0))) == "bool"

    with pytest.raises(TypeError, match="Cannot compare"):
        checker.visit(NotEqualExpr(StringLiteral("a"), BoolLiteral(True)))


def test_ordered_comparisons():
    checker = make_checker()

    assert checker.visit(GreaterExpr(IntLiteral(2), IntLiteral(1))) == "bool"
    assert checker.visit(LessExpr(IntLiteral(1), FloatLiteral(2.0))) == "bool"
    assert checker.visit(GreaterEqualExpr(FloatLiteral(2.0), IntLiteral(2))) == "bool"
    assert checker.visit(LessEqualExpr(IntLiteral(2), FloatLiteral(2.0))) == "bool"

    with pytest.raises(TypeError, match="Cannot compare"):
        checker.visit(GreaterExpr(StringLiteral("a"), IntLiteral(1)))

    with pytest.raises(TypeError, match="Cannot compare"):
        checker.visit(LessExpr(BoolLiteral(True), IntLiteral(1)))


# -------------------------
# boolean operators
# -------------------------

def test_and_expr():
    checker = make_checker()

    assert checker.visit(AndExpr(BoolLiteral(True), BoolLiteral(False))) == "bool"

    with pytest.raises(TypeError, match="AND requires bool"):
        checker.visit(AndExpr(IntLiteral(1), BoolLiteral(False)))


def test_or_expr():
    checker = make_checker()

    assert checker.visit(OrExpr(BoolLiteral(True), BoolLiteral(False))) == "bool"

    with pytest.raises(TypeError, match="OR requires bool"):
        checker.visit(OrExpr(StringLiteral("a"), BoolLiteral(False)))


def test_not_expr():
    checker = make_checker()

    assert checker.visit(NotExpr(BoolLiteral(True))) == "bool"

    with pytest.raises(TypeError, match="NOT requires bool"):
        checker.visit(NotExpr(IntLiteral(1)))


def test_xor_expr():
    checker = make_checker()

    assert checker.visit(XorExpr(BoolLiteral(True), BoolLiteral(False))) == "bool"

    with pytest.raises(TypeError, match="XOR requires bool"):
        checker.visit(XorExpr(BoolLiteral(True), IntLiteral(1)))


# -------------------------
# between / chance
# -------------------------

def test_between():
    checker = make_checker()

    assert checker.visit(Between(IntLiteral(1), IntLiteral(10))) == "bool"
    assert checker.visit(Between(FloatLiteral(1.5), IntLiteral(10))) == "bool"

    with pytest.raises(TypeError, match="between requires numeric types"):
        checker.visit(Between(StringLiteral("a"), IntLiteral(10)))


def test_chance():
    checker = make_checker()

    assert checker.visit(Chance(IntLiteral(30), IntLiteral(100))) == "bool"
    assert checker.visit(Chance(FloatLiteral(30.0), IntLiteral(100))) == "bool"

    with pytest.raises(TypeError, match="chance requires numeric types"):
        checker.visit(Chance(BoolLiteral(True), IntLiteral(100)))


# -------------------------
# if / while / dowhile
# -------------------------

def test_if_valid():
    checker = make_checker()

    node = If(
        BoolLiteral(True),
        [CreateVariable("x", IntLiteral(1))],
        [(BoolLiteral(False), [CreateVariable("y", IntLiteral(2))])],
        [CreateVariable("z", IntLiteral(3))]
    )

    assert checker.visit(node) is None


def test_if_invalid_condition():
    checker = make_checker()

    node = If(
        IntLiteral(1),
        [CreateVariable("x", IntLiteral(1))],
        [],
        []
    )

    with pytest.raises(TypeError, match="if leftition must be bool"):
        checker.visit(node)


def test_if_invalid_elif_condition():
    checker = make_checker()

    node = If(
        BoolLiteral(True),
        [],
        [(IntLiteral(1), [CreateVariable("x", IntLiteral(1))])],
        []
    )

    with pytest.raises(TypeError, match="elif leftition must be bool"):
        checker.visit(node)


def test_if_creates_variable():
    checker = make_checker()

    node = If(
        BoolLiteral(True),
        [CreateVariable("x", IntLiteral(1))],
        [],
        []
    )

    checker.visit(node)

    assert "x" in checker.v_table
    assert checker.v_table["x"] == "int"


def test_if_else_creates_variable():
    checker = make_checker()

    node = If(
        BoolLiteral(False),
        [],
        [],
        [CreateVariable("y", IntLiteral(2))]
    )

    checker.visit(node)

    assert "y" in checker.v_table
    assert checker.v_table["y"] == "int"


def test_if_none_condition_skips_body():
    checker = make_checker()
    checker.v_table["cond"] = None

    node = If(
        Var("cond", None),
        [CreateVariable("x", IntLiteral(1))],
        [],
        []
    )

    assert checker.visit(node) is None
    assert "x" not in checker.v_table


def test_while_valid_and_scope_restored():
    checker = make_checker()
    checker.v_table["cond"] = "bool"

    node = While(
        Var("cond", None),
        [CreateVariable("x", IntLiteral(1))]
    )

    assert checker.visit(node) is None
    assert "x" not in checker.v_table


def test_while_invalid_condition():
    checker = make_checker()
    checker.v_table["cond"] = "int"

    node = While(
        Var("cond", None),
        []
    )

    with pytest.raises(TypeError, match="while leftition must be bool"):
        checker.visit(node)


def test_dowhile_valid_and_scope_restored():
    checker = make_checker()
    checker.v_table["cond"] = "bool"

    node = Dowhile(
        [CreateVariable("x", IntLiteral(1))],
        Var("cond", None)
    )

    assert checker.visit(node) is None
    assert "x" not in checker.v_table


def test_dowhile_invalid_condition():
    checker = make_checker()
    checker.v_table["cond"] = "int"

    node = Dowhile(
        [CreateVariable("x", IntLiteral(1))],
        Var("cond", None)
    )

    with pytest.raises(TypeError, match="dowhile leftition must be bool"):
        checker.visit(node)


# -------------------------
# functions
# -------------------------

def test_define_function():
    checker = make_checker()

    node = Define(
        "Fun1",
        ["a", "b"],
        [Return(Add(Var("a", None), Var("b", None)))]
    )

    assert checker.visit(node) is None
    assert "Fun1" in checker.f_table


def test_define_duplicate_function_fails():
    checker = make_checker()

    node = Define("Fun1", [], [])
    checker.visit(node)

    with pytest.raises(TypeError, match="already exist"):
        checker.visit(node)


def test_call_missing_function_fails():
    checker = make_checker()

    with pytest.raises(TypeError, match="don't exist"):
        checker.visit(Call("Fun1", []))


def test_call_function_returns_type():
    checker = make_checker()

    checker.visit(
        Define(
            "Fun1",
            ["a", "b"],
            [Return(Add(Var("a", None), Var("b", None)))]
        )
    )

    result = checker.visit(Call("Fun1", [IntLiteral(1), FloatLiteral(2.0)]))
    assert result == "float"


def test_call_restores_scope():
    checker = make_checker()
    checker.v_table["outside"] = "str"

    checker.visit(
        Define(
            "Fun1",
            ["a"],
            [Return(Var("a", None))]
        )
    )

    checker.visit(Call("Fun1", [IntLiteral(1)]))

    assert checker.v_table["outside"] == "str"
    assert "a" not in checker.v_table


def test_define_function_without_params():
    checker = make_checker()

    node = Define(
        "Fun0",
        [],
        [Return(IntLiteral(1))]
    )

    assert checker.visit(node) is None
    assert "Fun0" in checker.f_table


def test_call_zero_arg_function_returns_type():
    checker = make_checker()

    checker.visit(
        Define(
            "Fun0",
            [],
            [Return(IntLiteral(1))]
        )
    )

    assert checker.visit(Call("Fun0", [])) == "int"


def test_call_function_without_return_returns_none():
    checker = make_checker()

    checker.visit(
        Define(
            "Fun1",
            ["a"],
            [CreateVariable("x", Var("a", None))]
        )
    )

    assert checker.visit(Call("Fun1", [IntLiteral(1)])) is None

# -------------------------
# lists
# -------------------------

def test_create_empty_list():
    checker = make_checker()

    assert checker.visit(CreateList("xs", None)) == "list"
    assert checker.v_table["xs"] == "list"


def test_create_typed_list():
    checker = make_checker()

    node = CreateList("xs", [IntLiteral(1), IntLiteral(2), IntLiteral(3)])
    assert checker.visit(node) == "list[int]"
    assert checker.v_table["xs"] == "list[int]"


def test_create_list_mixed_types_fails():
    checker = make_checker()

    node = CreateList("xs", [IntLiteral(1), StringLiteral("a")])

    with pytest.raises(TypeError, match="mixed types"):
        checker.visit(node)


def test_index_access_typed_list():
    checker = make_checker()
    checker.v_table["xs"] = "list[int]"

    node = IndexAccess(IntLiteral(0), Var("xs", None))
    assert checker.visit(node) == "int"


def test_index_access_generic_list_returns_none():
    checker = make_checker()
    checker.v_table["xs"] = "list"

    node = IndexAccess(IntLiteral(0), Var("xs", None))
    assert checker.visit(node) is None


def test_index_access_non_int_index_fails():
    checker = make_checker()
    checker.v_table["xs"] = "list[int]"

    node = IndexAccess(StringLiteral("0"), Var("xs", None))

    with pytest.raises(TypeError, match="List index must be int"):
        checker.visit(node)


def test_index_access_non_list_fails():
    checker = make_checker()
    checker.v_table["x"] = "int"

    node = IndexAccess(IntLiteral(0), Var("x", None))

    with pytest.raises(TypeError, match="Cannot index non-list type"):
        checker.visit(node)


def test_assign_to_list_index_valid():
    checker = make_checker()
    checker.v_table["xs"] = "list[int]"

    node = Assign(
        IndexAccess(IntLiteral(0), Var("xs", None)),
        None,
        IntLiteral(99)
    )

    assert checker.visit(node) == "int"


def test_assign_to_list_index_wrong_value_type_fails():
    checker = make_checker()
    checker.v_table["xs"] = "list[int]"

    node = Assign(
        IndexAccess(IntLiteral(0), Var("xs", None)),
        None,
        StringLiteral("oops")
    )

    with pytest.raises(TypeError, match="Cannot assign value of type"):
        checker.visit(node)

# -------------------------
# forloops
# -------------------------

def test_forrange_valid():
    checker = make_checker()

    node = Forrange(
        "i",
        IntLiteral(1),
        IntLiteral(10),
        [CreateVariable("x", IntLiteral(2))]
    )

    assert checker.visit(node) is None
    assert "i" not in checker.v_table
    assert "x" not in checker.v_table


def test_forrange_invalid_bounds():
    checker = make_checker()

    node = Forrange(
        "i",
        StringLiteral("a"),
        IntLiteral(10),
        []
    )

    with pytest.raises(TypeError, match="for-range bounds must be numeric"):
        checker.visit(node)


def test_foreach_valid():
    checker = make_checker()
    checker.v_table["xs"] = "list[int]"

    node = Foreach(
        "item",
        "xs",
        [CreateVariable("y", Add(Var("item", None), IntLiteral(1)))]
    )

    assert checker.visit(node) is None
    assert "item" not in checker.v_table
    assert "y" not in checker.v_table


def test_foreach_missing_collection_fails():
    checker = make_checker()

    node = Foreach("item", "xs", [])

    with pytest.raises(TypeError, match="don't exist"):
        checker.visit(node)


def test_foreach_non_list_fails():
    checker = make_checker()
    checker.v_table["xs"] = "int"

    node = Foreach("item", "xs", [])

    with pytest.raises(TypeError, match="Cannot iterate over non-list type"):
        checker.visit(node)

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