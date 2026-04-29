import pytest
from src.visitors.interpreter import *
from src.ast.nodes import *

def make_checker():
    return InterpreterVisitor()

def test_it_pass_arithmetic_basic():
    checker = make_checker()
    
    # 6^8*(2+1)
    node = Mul(Pow(IntLiteral(6),IntLiteral(2)),Add(IntLiteral(2),IntLiteral(1)))
    
    assert checker.visit(node) == 108

def test_it_pass_arithmetic_list_call():
    checker = make_checker()
    
    # (2-Y())^(X[0]*2)/5
    nodes = [
        CreateVariable("Answer"),
        CreateList("X",[IntLiteral(1),IntLiteral(2),IntLiteral(3)]),
        Define("Y",[],[Return(IntLiteral(3))]),
        Assign("Answer",None,Div(Pow(Add(IntLiteral(2),Neg(Call("Y"))),Mul(IndexAccess([IntLiteral(0)],"X"),IntLiteral(2))),IntLiteral(5)))
        ]
    checker.visit(nodes)
    
    assert checker.lookup("Answer") == 0.2

def test_it_pass_arithmetic_var_struct():
    checker = make_checker()
    
    # ((Y.Z+X*(4+1))^Y.Z-(8/(Y.Z+Y.Z)*(X+5)))+((6^Y.Z-4*X)/(1+1))^Y.Z
    nodes = [
        CreateVariable("Answer"),
        CreateVariable("X",IntLiteral(3)),
        CreateStruct("Y",[None,[CreateVariable("Z",IntLiteral(2))]]),
        Assign("Answer", None, Add(Add(Pow(Add(Var("Z","Y"),Mul(Var("X"),Add(IntLiteral(4),IntLiteral(1)))),Var("Z","Y")),Neg(Mul(Div(IntLiteral(8),Add(Var("Z","Y"),Var("Z","Y"))),Add(Var("X"),IntLiteral(5))))),Pow(Div(Add(Pow(IntLiteral(6),Var("Z","Y")),Neg(Mul(IntLiteral(4),Var("X")))),Add(IntLiteral(1),IntLiteral(1))),Var("Z","Y"))))
    ]
    checker.visit(nodes)
    
    assert checker.lookup("Answer") == 417