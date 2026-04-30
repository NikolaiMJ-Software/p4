import pytest
from src.visitors.interpreter import *
from src.ast.nodes import *

def make_checker():
    return InterpreterVisitor()

def test_or_true():
    checker = make_checker()
    
    node = OrExpr(BoolLiteral(True), BoolLiteral(False))
    
    assert checker.unwrap(checker.visit(node)) is True

def test_or_false():
    checker = make_checker()
    
    node = OrExpr(BoolLiteral(False), BoolLiteral(False))
    
    assert checker.unwrap(checker.visit(node)) is False

def test_and_true():
    checker = make_checker()
    
    node = AndExpr(BoolLiteral(True), BoolLiteral(True))
    
    assert checker.unwrap(checker.visit(node)) is True

def test_and_false():
    checker = make_checker()
    
    node = AndExpr(BoolLiteral(True), BoolLiteral(False))
    
    assert checker.unwrap(checker.visit(node)) is False

def test_xor_true():
    checker = make_checker()
    
    node = XorExpr(BoolLiteral(True), BoolLiteral(False))
    
    assert checker.unwrap(checker.visit(node)) is True

def test_xor_false():
    checker = make_checker()
    
    node = XorExpr(BoolLiteral(True), BoolLiteral(True))
    
    assert checker.unwrap(checker.visit(node)) is False

def test_not_true():
    checker = make_checker()
    
    node = NotExpr(BoolLiteral(False))
    
    assert checker.unwrap(checker.visit(node)) is True

def test_not_false():
    checker = make_checker()
    
    node = NotExpr(BoolLiteral(True))
    
    assert checker.unwrap(checker.visit(node)) is False

def test_equal_true():
    checker = make_checker()
    
    node = EqualExpr(IntLiteral(1), IntLiteral(1))
    
    assert checker.unwrap(checker.visit(node)) is True

def test_equal_false():
    checker = make_checker()
    
    node = EqualExpr(IntLiteral(1), IntLiteral(2))
    
    assert checker.unwrap(checker.visit(node)) is False

def test_notequal_true():
    checker = make_checker()
    
    node = NotEqualExpr(IntLiteral(1), IntLiteral(2))
    
    assert checker.unwrap(checker.visit(node)) is True

def test_notequal_false():
    checker = make_checker()
    
    node = NotEqualExpr(IntLiteral(1), IntLiteral(1))
    
    assert checker.unwrap(checker.visit(node)) is False

def test_greater_true():
    checker = make_checker()
    
    node = GreaterExpr(IntLiteral(1), IntLiteral(0))
    
    assert checker.unwrap(checker.visit(node)) is True

def test_greater_false():
    checker = make_checker()
    
    node = GreaterExpr(IntLiteral(0), IntLiteral(1))
    
    assert checker.unwrap(checker.visit(node)) is False

def test_less_true():
    checker = make_checker()
    
    node = LessExpr(IntLiteral(0), IntLiteral(1))
    
    assert checker.unwrap(checker.visit(node)) is True

def test_less_false():
    checker = make_checker()
    
    node = LessExpr(IntLiteral(1), IntLiteral(0))
    
    assert checker.unwrap(checker.visit(node)) is False

def test_greaterequal_true():
    checker = make_checker()
    
    node = GreaterEqualExpr(IntLiteral(1), IntLiteral(1))
    
    assert checker.unwrap(checker.visit(node)) is True

def test_greaterequal_false():
    checker = make_checker()
    
    node = GreaterEqualExpr(IntLiteral(0), IntLiteral(1))
    
    assert checker.unwrap(checker.visit(node)) is False

def test_lessequal_true():
    checker = make_checker()
    
    node = LessEqualExpr(IntLiteral(1), IntLiteral(1))
    
    assert checker.unwrap(checker.visit(node)) is True

def test_lessequal_false():
    checker = make_checker()
    
    node = LessEqualExpr(IntLiteral(1), IntLiteral(0))
    
    assert checker.unwrap(checker.visit(node)) is False

def test_add():
    checker = make_checker()
    
    node = Add(IntLiteral(1), IntLiteral(1))
    
    assert checker.unwrap(checker.visit(node)) == 2

def test_mul():
    checker = make_checker()
    
    node = Mul(IntLiteral(2), IntLiteral(2))
    
    assert checker.unwrap(checker.visit(node)) == 4

def test_div():
    checker = make_checker()
    
    node = Div(IntLiteral(2), IntLiteral(2))
    
    assert checker.unwrap(checker.visit(node)) == 1

def test_div_Error():
    checker = make_checker()
    
    node = Div(IntLiteral(2), IntLiteral(0))
    
    with pytest.raises(InterpreterError, match="division by 0"):
        checker.visit(node)

def test_pow():
    checker = make_checker()
    
    node = Pow(IntLiteral(2), IntLiteral(3))
    
    assert checker.unwrap(checker.visit(node)) == 8

def test_neg():
    checker = make_checker()
    
    node = Neg(IntLiteral(1))
    
    assert checker.unwrap(checker.visit(node)) == -1

def test_between(): # Have to seed to make test deterministic
    checker = make_checker()
    random.seed(0)
    
    node = Between(IntLiteral(1), IntLiteral(10))
    
    assert checker.unwrap(checker.visit(node)) == 7

def test_chance(): # Have to seed to make test deterministic
    checker = make_checker()
    random.seed(0)
    
    node = Chance(IntLiteral(1), IntLiteral(2))
    
    assert checker.unwrap(checker.visit(node)) is False

def test_var():
    checker = make_checker()
    
    checker.v_table = {"X":int(1)}
    node = Var("X")
    
    assert checker.unwrap(checker.visit(node)) == 1

def test_var_struct():
    checker = make_checker()
    
    checker.v_table = {"X":{"Y":int(1)}}
    node = Var("Y","X")
    
    assert checker.unwrap(checker.visit(node)) == 1

def test_call(capsys):
    checker = make_checker()
    
    checker.f_table = {"X":{"params":["Y"], "body":[Output([Var("Y")])]}}
    nodes = [
        Call("X", [IntLiteral(1)]),
        Call("X", [IntLiteral(2)])
    ]
    checker.visit(nodes)
    
    captured = capsys.readouterr()
    assert captured.out.strip().splitlines() == ["1", "2"]

def test_call_return(capsys):
    checker = make_checker()
    
    checker.f_table = {"X":{"params":[], "body":[
        Output([StringLiteral("1")]),
        Return(),
        Output([StringLiteral("2")])]}}
    node = Call("X", [])
    checker.visit(node)
    
    captured = capsys.readouterr()
    assert captured.out.strip() == "1"

def test_indexaccess():
    checker = make_checker()
    
    checker.v_table = {"X":[int(1),int(2),int(3),int(4),int(5)]}
    node = IndexAccess([IntLiteral(0)], "X")
    
    assert checker.unwrap(checker.visit(node)) == 1

def test_indexaccess_struct():
    checker = make_checker()
    
    checker.v_table = {"X":{"Z":[[int(1),int(2),int(3)],int(4),int(5)]}}
    node = IndexAccess([IntLiteral(1), IntLiteral(0)], "Z", "X")
    
    assert checker.unwrap(checker.visit(node)) == 2