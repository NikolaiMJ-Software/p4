import pytest
from src.visitors.interpreter import *
from src.ast.nodes import *

def make_checker():
    return InterpreterVisitor()

def test_it_pass_create_and_assign_variable():
    checker = make_checker()

    nodes = [
        CreateVariable("X", IntLiteral(10)),
        Assign("X", None, Add(Var("X"), IntLiteral(5)))
    ]

    checker.visit(nodes)

    assert checker.unwrap(checker.lookup_var("X")) == 15

def test_it_pass_create_and_assign_list():
    checker = make_checker()

    nodes = [
        CreateList("X", [IntLiteral(10), StringLiteral("Ola"), FloatLiteral(5.5)]),
        AssignIndex(
            IndexAccess([IntLiteral(0)], "X"),IntLiteral(2)
        )
    ]

    checker.visit(nodes)

    assert checker.unwrap_list(checker.lookup_var("X")) == [2,"Ola",5.5]

def test_it_pass_create_struct_and_assign_struct_field():
    checker = make_checker()

    nodes = [
        CreateStruct("X", [None, [
            CreateVariable("Y", StringLiteral("nej")),
            CreateVariable("Z", IntLiteral(3))
            ]]),
            Assign("Y", "X", IntLiteral(4))
    ]

    checker.visit(nodes)

    assert checker.unwrap(checker.lookup_var("X")["Y"]) == 4
    assert checker.unwrap(checker.lookup_var("X")["Z"]) == 3

def test_it_assign_if_statement():
    checker = make_checker()
    
    node = [
        CreateVariable("X", None),
        If(BoolLiteral(True),[
            Assign("X", None, IntLiteral(10))
        ],[],[])
    ]
    
    checker.visit(node)
    
    assert checker.unwrap(checker.lookup_var("X")) == 10
    
def test_while_loop_with_break_stmt():
    
    checker = make_checker()
    
    node = [
        CreateVariable("X", IntLiteral(0)),
        While(BoolLiteral(True),[
            Assign("X", None, Add(Var("X"), IntLiteral(1))),
            If(EqualExpr(Var("X"), IntLiteral(10)), [
                Break()
            ],[],[])
        ])
    ]
    
    checker.visit(node)
    
    assert checker.unwrap(checker.lookup_var("X")) == 10
    

def test_do_while_loop():
    checker = make_checker()
    
    node = [
        CreateVariable("X", IntLiteral(0)),
        Dowhile([
            Assign("X", None, Add(Var("X"), IntLiteral(3)))
            ], LessEqualExpr(Var("X"), IntLiteral(10)))
    ]
    
    checker.visit(node)
    
    assert checker.unwrap(checker.lookup_var("X")) == 12

#needs to be done: else if, else, function creation/call, return, forrange, foreach, input, output