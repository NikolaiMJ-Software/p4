import pytest
from src.visitors.interpreter import *
from src.ast.nodes import *

def make_checker():
    return InterpreterVisitor()

def test_gamestate_saveload():
    checker = make_checker()
    
    node = CreateStruct("Game",[None,[CreateVariable("X",IntLiteral(1))]])
    checker.visit(node)
    checker.save_game_state()
    checker.v_table = {"Game":None}
    checker.load_game_state()
    
    assert str(checker.v_table) == str({"Game":{"X":RuntimeValue("int",1)}})

def test_run(capsys):
    checker = make_checker()
    
    nodes = [
        CreateVariable("X",IntLiteral(1)),
        Define("Play",[],[Output([Var("X")])])
        ]
    checker.run(nodes)
    
    captured = capsys.readouterr()
    assert captured.out.strip() == "1"