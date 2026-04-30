import pytest
from src.visitors.interpreter import *
from src.ast.nodes import *

def make_checker():
    return InterpreterVisitor()

def test_it_boolean_basic_true():
    checker = make_checker()
    
    # True and True or True xor True
    node = OrExpr(AndExpr(BoolLiteral(True),BoolLiteral(True)),BoolLiteral(False))
    
    assert str(checker.visit(node)) == str(RuntimeValue("bool",True))

def test_it_boolean_basic_false():
    checker = make_checker()
    
    # True and False or True xor True
    node = OrExpr(AndExpr(BoolLiteral(True),BoolLiteral(False)),XorExpr(BoolLiteral(False),BoolLiteral(False)))
    
    assert str(checker.visit(node)) == str(RuntimeValue("bool",False))

def test_it_boolean_comparison_true():
    checker = make_checker()
    
    # ((8>1)==(7>=7)) or (5<2 and 1<=9)
    node = OrExpr(EqualExpr(GreaterExpr(IntLiteral(8),IntLiteral(1)),GreaterEqualExpr(IntLiteral(7),IntLiteral(7))),AndExpr(LessExpr(IntLiteral(5),IntLiteral(2)),LessEqualExpr(IntLiteral(1),IntLiteral(9))))
    
    assert str(checker.visit(node)) == str(RuntimeValue("bool",True))

def test_it_boolean_comparison_false():
    checker = make_checker()
    
    # ((1>8)==(7>=7)) or (5<2 and 1<=9)
    node = OrExpr(EqualExpr(GreaterExpr(IntLiteral(1),IntLiteral(8)),GreaterEqualExpr(IntLiteral(7),IntLiteral(7))),AndExpr(LessExpr(IntLiteral(5),IntLiteral(2)),LessEqualExpr(IntLiteral(1),IntLiteral(9))))
    
    assert str(checker.visit(node)) == str(RuntimeValue("bool",False))
    
def test_it_pass_arithmetic_basic():
    checker = make_checker()
    
    # 6^8*(2+1)
    node = Mul(Pow(IntLiteral(6),IntLiteral(2)),Add(IntLiteral(2),IntLiteral(1)))
    
    assert str(checker.visit(node)) == str(RuntimeValue("int",108))

def test_it_pass_arithmetic_list_call():
    checker = make_checker()
    
    # (2-Y())^(X[0]*2)/5
    nodes = [
        CreateVariable("Answer"),
        CreateList("X",[IntLiteral(1),IntLiteral(2),IntLiteral(3)]),
        Define("Y",None,[Return(IntLiteral(3))]),
        Assign("Answer",None,Div(Pow(Add(IntLiteral(2),Neg(Call("Y"))),Mul(IndexAccess([IntLiteral(0)],"X"),IntLiteral(2))),IntLiteral(5)))
        ]
    checker.visit(nodes)
    
    assert checker.lookup_var("Answer") == float(0.2)

def test_it_pass_arithmetic_var_struct_between():
    checker = make_checker()
    random.seed(0) # need to seed between to avoid randomness in tests
    
    # ((Y.Z+X*(4+random(1,10)))^Y.Z-(8/(Y.Z+Y.Z)*(X+5)))+((6^Y.Z-4*X)/(1+1))^Y.Z
    nodes = [
        CreateVariable("Answer"),
        CreateVariable("X",IntLiteral(3)),
        CreateStruct("Y",[None,[CreateVariable("Z",IntLiteral(2))]]),
        Assign("Answer", None, Add(Add(Pow(Add(Var("Z","Y"),Mul(Var("X"),Add(IntLiteral(4),Between(IntLiteral(1),IntLiteral(10))))),Var("Z","Y")),Neg(Mul(Div(IntLiteral(8),Add(Var("Z","Y"),Var("Z","Y"))),Add(Var("X"),IntLiteral(5))))),Pow(Div(Add(Pow(IntLiteral(6),Var("Z","Y")),Neg(Mul(IntLiteral(4),Var("X")))),Add(IntLiteral(1),IntLiteral(1))),Var("Z","Y"))))
    ]
    checker.visit(nodes)
    
    assert checker.lookup_var("Answer") == int(1353)