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


def test_neg():
    checker = make_checker()

    assert checker.visit(Neg(IntLiteral(2))) == "int"
    assert checker.visit(Neg(FloatLiteral(2.5))) == "float"
    assert checker.visit(Neg(Neg(IntLiteral(2)))) == "int"
    assert checker.visit(Neg(Neg(FloatLiteral(2.5)))) == "float"

    with pytest.raises(TypeError, match="NEG requires numeric type"):
        checker.visit(Neg(StringLiteral("hello")))

    with pytest.raises(TypeError, match="NEG requires numeric type"):
        checker.visit(Neg(BoolLiteral(True)))


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
# Input / Output
# -------------------------
def test_input():
    checker = make_checker()
    
    # X not initilized
    with pytest.raises(TypeError, match="does not exist"):
        checker.visit(Input("X"))
    
    # X are initilized
    nodes = [CreateVariable("X", None),Input("X")]
    for node in nodes:
        checker.visit(node)

def test_output():
    checker = make_checker()
    # X not initilized
    with pytest.raises(TypeError, match="does not exist"):
        checker.visit(Output([StringLiteral("Hello"), Var("X", None), IntLiteral(5)]))
    
    # X are initilized
    nodes = [CreateVariable("X", None),Output([StringLiteral("Hello"), Var("X", None)])]
    for node in nodes:
        checker.visit(node)

# -------------------------
# Expression / Break
# -------------------------
def test_expression():
    checker = make_checker()

    assert checker.visit(Expression(IntLiteral(2))) == "int"
    assert checker.visit(Expression(FloatLiteral(2.5))) == "float"
    assert checker.visit(Expression(StringLiteral("hello"))) == "str"
    assert checker.visit(Expression(BoolLiteral(True))) == "bool"
    assert checker.visit(Expression(Add(IntLiteral(2), IntLiteral(3)))) == "int"

    checker.visit(CreateVariable("X", IntLiteral(5)))
    assert checker.visit(Expression(Var("X", None))) == "int"

    with pytest.raises(TypeError, match="does not exist"):
        checker.visit(Expression(Var("Y", None)))

def test_break():
    checker = make_checker()

    assert checker.visit(Break()) is None