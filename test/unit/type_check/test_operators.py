import pytest
from src.visitors.type_checker.type_checker import *
from src.ast.nodes import *

# -------------------------
# basic helpers / literals
# -------------------------
def test_is_numeric():
    assert TypeChecker().is_numeric("int") is True
    assert TypeChecker().is_numeric("float") is True
    assert TypeChecker().is_numeric("str") is False
    assert TypeChecker().is_numeric("bool") is False
    assert TypeChecker().is_numeric(None) is False


def test_numeric_result_type():
    assert TypeChecker().numeric_result_type(None, "+", "int", "int") == "int"
    assert TypeChecker().numeric_result_type(None, "+", "int", "float") == "float"
    assert TypeChecker().numeric_result_type(None, "+", "float", "int") == "float"
    assert TypeChecker().numeric_result_type(None, "+", "float", "float") == "float"

    with pytest.raises(TypeError, match="Expected numeric types"):
        TypeChecker().numeric_result_type(None, "+", "str", "int")

# -------------------------
# arithmetic
# -------------------------

def test_add():
    assert TypeChecker().check_add(Add(IntLiteral(2), IntLiteral(2)), "int", "int") == "int"
    assert TypeChecker().check_add(Add(FloatLiteral(2.0), FloatLiteral(2.0)), "float", "float") == "float"
    assert TypeChecker().check_add(Add(IntLiteral(2), FloatLiteral(2.0)), "int", "float") == "float"
    assert TypeChecker().check_add(Add(FloatLiteral(2.0), IntLiteral(2)), "float", "int") == "float"
    assert TypeChecker().check_add(Add(StringLiteral("a"), StringLiteral("b")), "str", "str") == "str"

    with pytest.raises(TypeError, match="Expected numeric types"):
        TypeChecker().check_add(Add(StringLiteral("a"), IntLiteral(2)), "str", "int")


def test_neg():
    assert TypeChecker().check_neg(Neg(IntLiteral(2)), "int") == "int"
    assert TypeChecker().check_neg(Neg(FloatLiteral(2.5)), "float") == "float"

    with pytest.raises(TypeError, match="NEG requires numeric type"):
        TypeChecker().check_neg(Neg(StringLiteral("hello")), "str")

    with pytest.raises(TypeError, match="NEG requires numeric type"):
        TypeChecker().check_neg(Neg(BoolLiteral(True)), "bool")


def test_mul():
    assert TypeChecker().check_mul(Mul(IntLiteral(2), IntLiteral(2)), "int", "int") == "int"
    assert TypeChecker().check_mul(Mul(IntLiteral(2), FloatLiteral(2.0)), "int", "float") == "float"

    with pytest.raises(TypeError, match="Expected numeric types"):
        TypeChecker().check_mul(Mul(StringLiteral("a"), IntLiteral(2)), "str", "int")


def test_div():
    assert TypeChecker().check_div(Div(IntLiteral(4), IntLiteral(2)), "int", "int") == "float"
    assert TypeChecker().check_div(Div(FloatLiteral(4.0), IntLiteral(2)), "float", "int") == "float"

    with pytest.raises(TypeError, match="Expected numeric types"):
        TypeChecker().check_div(Div(StringLiteral("a"), IntLiteral(2)), "str", "int")


def test_pow():
    assert TypeChecker().check_pow(Pow(IntLiteral(2), IntLiteral(3)), "int", "int") == "int"
    assert TypeChecker().check_pow(Pow(IntLiteral(2), FloatLiteral(3.0)), "int", "float") == "float"

    with pytest.raises(TypeError, match="Expected numeric types"):
        TypeChecker().check_pow(Pow(StringLiteral("a"), IntLiteral(2)), "str", "int")


# -------------------------
# comparisons
# -------------------------
def test_ordered_comparisons():
    node0 = GreaterExpr(IntLiteral(2), IntLiteral(1))
    node1 = LessExpr(IntLiteral(1), FloatLiteral(2.0))
    node2 = GreaterEqualExpr(FloatLiteral(2.0), IntLiteral(2))
    node3 = LessEqualExpr(IntLiteral(2), FloatLiteral(2.0))

    result0 = TypeChecker().check_comp_ops_expr(node0, ">", "int", "int")
    result1 = TypeChecker().check_comp_ops_expr(node1, "<", "int", "float")
    result2 = TypeChecker().check_comp_ops_expr(node2, ">=", "float", "int")
    result3 = TypeChecker().check_comp_ops_expr(node3, "<=", "int", "float")
    
    assert result0 == "bool"
    assert result1 == "bool"
    assert result2 == "bool"
    assert result3 == "bool"

    with pytest.raises(TypeError, match="Can't compare: 'str' > 'int'"):
        TypeChecker().check_comp_ops_expr(GreaterExpr(StringLiteral("a"), IntLiteral(1)), ">", "str", "int")

    with pytest.raises(TypeError, match="Can't compare: 'bool' < 'int'"):
        TypeChecker().check_comp_ops_expr(LessExpr(BoolLiteral(True), IntLiteral(1)), "<", "bool", "int")


# -------------------------
# boolean operators
# -------------------------
def test_bool_ops_expr():
    node = AndExpr(BoolLiteral(True), BoolLiteral(False))
    result = TypeChecker().check_bool_ops_expr(node, "AND", "bool", "bool")
    assert result == "bool"

    with pytest.raises(TypeError, match="AND requires bool, got 'int' and 'bool'"):
        TypeChecker().check_bool_ops_expr(AndExpr(IntLiteral(1), BoolLiteral(False)), "AND", "int", "bool")

    with pytest.raises(TypeError, match="OR requires bool, got 'str' and 'bool'"):
        TypeChecker().check_bool_ops_expr(OrExpr(StringLiteral("a"), BoolLiteral(False)), "OR", "str", "bool")

    with pytest.raises(TypeError, match="NOT requires bool, got 'int'"):
        TypeChecker().check_bool_ops_expr(NotExpr(IntLiteral(1)), "NOT", "int")

    with pytest.raises(TypeError, match="XOR requires bool, got 'bool' and 'float'"):
        TypeChecker().check_bool_ops_expr(XorExpr(BoolLiteral(True), FloatLiteral(1.0)), "XOR", "bool", "float")


# -------------------------
# between / chance
# -------------------------
def test_between():
    node0 = Between(IntLiteral(30), IntLiteral(100))
    node1 = Between(FloatLiteral(30.0), IntLiteral(100))
    node2 = Between(IntLiteral(100), FloatLiteral(30.0))
    node3 = Between(IntLiteral(100), StringLiteral("30"))
    node4 = Between(StringLiteral("30"), BoolLiteral(True))

    result0 = TypeChecker().check_between(node0, "int", "int")
    result1 = TypeChecker().check_between(node1, "float", "int")
    result2 = TypeChecker().check_between(node2, "int", "float")

    assert result0 == "int"
    assert result1 == "float"
    assert result2 == "float"
    with pytest.raises(TypeError, match="between requires numeric types, got 'int' and 'str'"):
        TypeChecker().check_between(node3, "int", "str")
    with pytest.raises(TypeError, match="between requires numeric types, got 'str' and 'bool'"):
        TypeChecker().check_between(node4, "str", "bool")

def test_chance():
    node0 = Chance(IntLiteral(30), IntLiteral(100))
    node1 = Chance(FloatLiteral(30.0), IntLiteral(100))
    node2 = Chance(IntLiteral(100), FloatLiteral(30.0))
    node3 = Chance(IntLiteral(100), StringLiteral("30"))
    node4 = Chance(StringLiteral("30"), BoolLiteral(True))

    result0 = TypeChecker().check_chance(node0, "int", "int")
    result1 = TypeChecker().check_chance(node1, "float", "int")
    result2 = TypeChecker().check_chance(node2, "int", "float")

    assert result0 == "bool"
    assert result1 == "bool"
    assert result2 == "bool"
    with pytest.raises(TypeError, match="chance requires numeric types, got 'int' and 'str'"):
        TypeChecker().check_chance(node3, "int", "str")
    with pytest.raises(TypeError, match="chance requires numeric types, got 'str' and 'bool'"):
        TypeChecker().check_chance(node4, "str", "bool")