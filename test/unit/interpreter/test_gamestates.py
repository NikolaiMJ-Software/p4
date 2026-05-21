import pytest
from end_to_end.setup_e2e import delete_save_file # Remove save file '999'
from src.visitors.interpreter.interpreter import InterpreterVisitor
from src.visitors.interpreter.runtime_value import RuntimeValue
from src.ast.nodes import *

def make_checker():
    return InterpreterVisitor(slot=999)

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