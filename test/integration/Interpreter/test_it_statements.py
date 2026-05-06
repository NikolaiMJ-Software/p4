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
    
def test_forrange_with_if_if_else_else_and_output(capsys):
    checker = make_checker()
    
    node = [
        CreateVariable("X", StringLiteral("Hej!, ")),
        Forrange("V",IntLiteral(1),IntLiteral(10),[
            If(EqualExpr(Var("X"),StringLiteral("Hej!, ")),[
                 Assign("X", None, Add(Var("X"), StringLiteral("med dig!, ")))
            ],[
                [EqualExpr(Var("X"), StringLiteral("Hej!, med dig!, ")),[Assign("X", None, Add(Var("X"), StringLiteral("the cake is a lie!")))]]],
            [
                Assign("X", None, Add(Var("X"), StringLiteral("!")))
            ])
        ]),
        Output([Var("X")])
    ]    
    
    checker.visit(node)
    
    text = capsys.readouterr()

    assert text.out.strip() == "Hej!, med dig!, the cake is a lie!!!!!!!!!"
    
    assert checker.unwrap(checker.lookup_var("X")) == "Hej!, med dig!, the cake is a lie!!!!!!!!!"

def test_foreach_from_list_including_input(monkeypatch, capsys):
    checker = make_checker()

    monkeypatch.setattr("builtins.input", lambda: "Bye")

    node = [
        CreateList("List", [
            StringLiteral("Hello"),
            StringLiteral("Hello"),
            StringLiteral("Hello")
        ]),
        CreateVariable("Count", IntLiteral(0)),
        Foreach("Element", "List", [
            Input([], "Element", None),
            AssignIndex(
                IndexAccess([Var("Count")], "List", None), Var("Element")),
            Assign("Count", None, Add(Var("Count"), IntLiteral(1)))        ]),
        Output([Var("List")])
    ]

    checker.visit(node)

    captured = capsys.readouterr()
    assert captured.out.strip().splitlines() == [
        "['Bye', 'Bye', 'Bye']"
    ]

def test_forrange_from_list_including_input(monkeypatch):
    checker = make_checker()

    monkeypatch.setattr("builtins.input", lambda: "Bye")

    node = [
        CreateList("List", [
            StringLiteral("Hello"),
            StringLiteral("Hello"),
            StringLiteral("Hello")
        ]),
        Forrange("Index", IntLiteral(0), IntLiteral(2), [
            Input([Var("Index")], "List", None)
        ])
    ]

    checker.visit(node)

    assert checker.unwrap_list(checker.lookup_var("List")) == ["Bye", "Bye", "Bye"]

def test_func_create_call_no_params():
    checker = make_checker()
    
    nodes = [
        CreateVariable("X", FloatLiteral(5.5)),
        Define("Func", [], [
            Assign("X", None, Add(Var("X"), FloatLiteral(1.2)))
        ]),
        Call("Func", [])
    ]
    
    checker.visit(nodes)
    
    assert checker.unwrap(checker.lookup_var("X")) == 6.7


def test_func_create_call_return_params():
    checker = make_checker()
    
    nodes = [
        Define("Func", ["A", "B"], [
            CreateVariable("Y", Add(Var("A"), Var("B"))),
            Return(Var("Y"))
        ]),
        CreateVariable("X", Call("Func", [IntLiteral(2), IntLiteral(3)]))
    ]
    
    checker.visit(nodes)
    
    assert checker.unwrap(checker.lookup_var("X")) == 5

