import pytest
from src.visitors.interpreter import *
from src.ast.nodes import *

def make_checker():
    return InterpreterVisitor()

def test_create_variable():
    checker = make_checker()
    
    node = CreateVariable("X")
    checker.visit(node)
    
    assert checker.v_table == {"X":"UNINITIALIZED"}

def test_create_variable_withvalue():
    checker = make_checker()
    
    node = CreateVariable("X", IntLiteral(1))
    checker.visit(node)
    
    assert str(checker.v_table) == str({"X":RuntimeValue("int",1)})

def test_create_struct():
    checker = make_checker()
    
    node = CreateStruct("X", [None,[CreateVariable("Y"), CreateVariable("Z", IntLiteral(1))]])
    checker.visit(node)

    assert str(checker.v_table) == str({"X":{"Y":"UNINITIALIZED","Z":RuntimeValue("int",1)}})

def test_create_struct_withbase():
    checker = make_checker()
    
    checker.v_table = {"A":{"B":RuntimeValue("int",1),"C":RuntimeValue("int",2)}}
    node = CreateStruct("X", ["A",[CreateVariable("Y"), CreateVariable("Z", IntLiteral(1))]])
    checker.visit(node)
    
    assert str(checker.v_table) == str({"A":{"B":RuntimeValue("int",1),"C":RuntimeValue("int",2)}, "X":{"B":RuntimeValue("int",1),"C":RuntimeValue("int",2),"Y":"UNINITIALIZED","Z":RuntimeValue("int",1)}})

def test_create_list():
    checker = make_checker()
    
    node = CreateList("X", [BoolLiteral(1), IntLiteral(2), StringLiteral("3")])
    checker.visit(node)
    
    assert str(checker.v_table) == str({"X":[RuntimeValue("bool",1),RuntimeValue("int",2),RuntimeValue("str","3")]})

def test_assign():
    checker = make_checker()
    
    checker.v_table = {"X":RuntimeValue("int",1)}
    node = Assign("X", None, IntLiteral(2))
    checker.visit(node)
    
    assert str(checker.v_table) == str({"X":RuntimeValue("int",2)})

def test_assign_struct():
    checker = make_checker()
    
    checker.v_table = {"X":{"Y":RuntimeValue("int",1),"Z":RuntimeValue("int",2)}}
    node = Assign("Z","X",IntLiteral(3))
    checker.visit(node)
    
    assert str(checker.v_table) == str({"X":{"Y":RuntimeValue("int",1),"Z":RuntimeValue("int",3)}})

def test_assign_parent():
    checker = make_checker()
    
    checker.v_table = {"__parent__":{"X":RuntimeValue("int",1)}}
    node = Assign("X",None,IntLiteral(2))
    checker.visit(node)
    
    assert str(checker.v_table) == str({"__parent__":{"X":RuntimeValue("int",2)}})

def test_assignindex():
    checker = make_checker()
    
    # insert list X:[[1,[2,3],4],5]
    checker.v_table = {"X":[[RuntimeValue("int",1),[RuntimeValue("int",2),RuntimeValue("int",3)],RuntimeValue("int",4)],RuntimeValue("int",5)]}
    # assign X[0][1][1] = 0    (this would 3 exchanged for 0)
    node = AssignIndex(IndexAccess([IntLiteral(1),IntLiteral(1),IntLiteral(0)],"X",None),IntLiteral(0))
    checker.visit(node)
    
    assert str(checker.v_table) == str({"X":[[RuntimeValue("int",1),[RuntimeValue("int",2),RuntimeValue("int",0)],RuntimeValue("int",4)],RuntimeValue("int",5)]})

def test_assignindex_struct():
    checker = make_checker()
    
    checker.v_table = {"X":{"Y":[[RuntimeValue("int",1),RuntimeValue("int",2)],RuntimeValue("int",3)]}}
    node = AssignIndex(IndexAccess([IntLiteral(1),IntLiteral(0)],"Y","X"),IntLiteral(0))
    checker.visit(node)
   
    assert str(checker.v_table) == str({"X":{"Y":[[RuntimeValue("int",1),RuntimeValue("int",0)],RuntimeValue("int",3)]}})

def test_if_base(capsys):
    checker = make_checker()
    
    node = If(BoolLiteral(True),
                [Output([StringLiteral("Base")])],
            None,
            None)
    checker.visit(node)
    
    captured = capsys.readouterr()
    assert captured.out.strip() == "Base"

def test_if_elif(capsys):
    checker = make_checker()
    
    node = If(BoolLiteral(False), [
                Output([StringLiteral("Base")])],
            [[BoolLiteral(False), [
                Output([StringLiteral("Elif1")])]],
            [BoolLiteral(True), [
                Output([StringLiteral("Elif2")])]]],
            None)
    checker.visit(node)
    
    captured = capsys.readouterr()
    assert captured.out.strip() == "Elif2"

def test_if_else(capsys):
    checker = make_checker()
    
    node = If(BoolLiteral(False), [
                Output([StringLiteral("Base")])],
            [[BoolLiteral(False), [
                Output([StringLiteral("Elif1")])]],
            [BoolLiteral(False), [
                Output([StringLiteral("Elif2")])]]],
            [Output([StringLiteral("Else")])])
    checker.visit(node)
    
    captured = capsys.readouterr()
    assert captured.out.strip() == "Else"

def test_while():
    checker = make_checker()
    
    checker.v_table = {"X":RuntimeValue("int",0)}
    node = While(LessExpr(Var("X"), IntLiteral(3)), [
        Assign("X", None, Add(Var("X"), IntLiteral(1)))
    ])
    checker.visit(node)
    
    assert str(checker.v_table) == str({"X":RuntimeValue("int",3)})

def test_while_break(capsys):
    checker = make_checker()
    
    checker.v_tables = [{"X":0}]
    node = While(BoolLiteral(True), [
        Output([StringLiteral("1")]),
        Break(),
        Output([StringLiteral("2")])
    ])
    checker.visit(node)
    
    captured = capsys.readouterr()
    assert captured.out.strip() == "1"

def test_dowhile():
    checker = make_checker()
    
    checker.v_table = {"X":RuntimeValue("int",0)}
    node = Dowhile(
        [Assign("X", None, Add(Var("X"), IntLiteral(1)))],
        LessExpr(Var("X"), IntLiteral(3)))
    checker.visit(node)
    
    assert str(checker.v_table) == str({"X":RuntimeValue("int",3)})

def test_dowhile_break(capsys):
    checker = make_checker()
    
    checker.v_tables = [{"X":0}]
    node = Dowhile([
        Output([StringLiteral("1")]),
        Break(),
        Output([StringLiteral("2")])],
        BoolLiteral(True))
    checker.visit(node)
    
    captured = capsys.readouterr()
    assert captured.out.strip() == "1"

def test_forrange(capsys):
    checker = make_checker()
    
    node = Forrange("X", IntLiteral(1), IntLiteral(3),[
        Output([Var("X")])
    ])
    checker.visit(node)
    
    captured = capsys.readouterr()
    assert captured.out.strip().splitlines() == ["1", "2", "3"]

def test_forrange_reverse(capsys):
    checker = make_checker()
    
    node = Forrange("X", IntLiteral(3), IntLiteral(1),[
        Output([Var("X")])
    ])
    checker.visit(node)
    
    captured = capsys.readouterr()
    assert captured.out.strip().splitlines() == ["3", "2", "1"]

def test_forrange_break(capsys):
    checker = make_checker()
    
    node = Forrange("X", IntLiteral(1), IntLiteral(2),[
        Output([IntLiteral(1)]),
        Break(),
        Output([IntLiteral(2)])
    ])
    checker.visit(node)
    
    captured = capsys.readouterr()
    assert captured.out.strip() == "1"

def test_foreach(capsys):
    checker = make_checker()
    
    checker.v_table = {"X":[RuntimeValue("int",1),RuntimeValue("int",2),RuntimeValue("int",3)]}
    node = Foreach("Y", "X", [
        Output([Var("Y")])
    ])
    checker.visit(node)
    
    captured = capsys.readouterr()
    assert captured.out.strip().splitlines() == ["1", "2", "3"]

def test_foreach_break(capsys):
    checker = make_checker()
    
    checker.v_table = {"X":[RuntimeValue("int",1),RuntimeValue("int",2),RuntimeValue("int",3)]}
    node = Foreach("Y", "X", [
        Output([Var("Y")]),
        Break()
    ])
    checker.visit(node)
    
    captured = capsys.readouterr()
    assert captured.out.strip() == "1"

def test_define():
    checker = make_checker()
    
    node = Define("X",None,[
        Output(StringLiteral("Test"))
    ])
    checker.visit(node)
    
    assert str(checker.f_table) == str({"X":{"params":None,"body":[Output(StringLiteral("Test"))]}})
    
def test_define_witharguments():
    checker = make_checker()
    
    node = Define("X", ["Y"], [
        Output([Var("Y")])
    ])
    checker.visit(node)
    
    assert str(checker.f_table) == str({"X":{"params":["Y"], "body":[Output([Var("Y")])]}})

def test_return():
    checker = make_checker()
    
    node = Return(StringLiteral("Test"))
    
    with pytest.raises(ReturnException, match="Test"):
        checker.visit(node)

# Would add break test here, but all applications have previously been tested for it.

def test_expression(capsys): # Could test more, but this is the main purpose of expression. rest is tested in test_expressions.py
    checker = make_checker()
    
    checker.f_table = {"X":{"params":[], "body":[Output([IntLiteral(1)])]}}
    node = Expression(Call("X"))
    checker.visit(node)
    
    captured = capsys.readouterr()
    assert captured.out.strip() == "1"

def test_input(monkeypatch):
    checker = make_checker()
    
    checker.v_table = {"X":RuntimeValue("int",0)}
    monkeypatch.setattr("builtins.input", lambda: 2)
    node = Input("X")
    checker.visit(node)
    
    assert str(checker.v_table) == str({"X":RuntimeValue("str",2)})

def test_output(capsys):
    checker = make_checker()
    
    node = Output([StringLiteral("Test")])
    checker.visit(node)
    
    captured = capsys.readouterr()
    assert captured.out.strip() == "Test"