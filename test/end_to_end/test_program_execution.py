import builtins

from src.ast import builder
from src.parser import parse
from src.visitors.interpreter import InterpreterVisitor


def run_program(code, monkeypatch, capsys, inputs=None, slot=999):
    inputs = iter(inputs or [])
    # monkeypatch is used to replace input 
    monkeypatch.setattr(builtins, "input", lambda: next(inputs))

    tree = parse(code)
    ast = builder.ASTBuilder().transform(tree)

    interp = InterpreterVisitor(code, slot=slot)
    interp.run(ast)
    # capsys will be used to capture what the program prints like "worked"
    return capsys.readouterr().out.strip().splitlines()


def test_e2e_input_then_string_comparison(monkeypatch, capsys):
    code = '''create Answer

define Play:
    input in Answer
    if Answer equal "yes" do:
        output "worked"
    else do:
        output "failed"
'''

    output = run_program(code, monkeypatch, capsys, inputs=["yes"])

    assert output == ["worked"]


def test_e2e_function_call_typechecks_dynamically(monkeypatch, capsys):
    code = '''create Answer

define Play:
    call Ask

define Ask:
    input in Answer
    if Answer equal "yes" do:
        output "accepted"
''' 

    output = run_program(code, monkeypatch, capsys, inputs=["yes"])

    assert output == ["accepted"]


def test_e2e_output_struct_field(monkeypatch, capsys):
    code = '''create Game with:
    Weapon
    Weapon_damage

define Play:
    Weapon from Game is "sword"
    Weapon_damage from Game is 10
    output "Weapon:", Weapon from Game, "Damage:", Weapon_damage from Game
'''

    output = run_program(code, monkeypatch, capsys, slot=997)

    assert output == ["Weapon: sword Damage: 10"]


def test_e2e_save_and_load_game_state(monkeypatch, capsys):
    slot = 996

    first_code = '''create Game with:
    Game_status is 0
    Name

define Play:
    Game_status from Game is 1
    Name from Game is "Bob"
    output "saved"
'''
    output = run_program(first_code, monkeypatch, capsys, slot=slot)

    assert output == ["saved"]

    second_code = '''create Game with:
    Game_status is 0
    Name

define Play:
    output Game_status from Game
    output Name from Game
'''

    output = run_program(second_code, monkeypatch, capsys, slot=slot)

    assert output == ["1", "Bob"]

def test_e2e_input_else_branch(monkeypatch, capsys):
    code = '''create Answer

define Play:
    input in Answer
    if Answer equal "yes" do:
        output "worked"
    else do:
        output "failed"
'''

    output = run_program(code, monkeypatch, capsys, inputs=["no"])

    assert output == ["failed"]


def test_e2e_loop_with_stop(monkeypatch, capsys):
    code = '''create Answer

define Play:
    while true do:
        input in Answer
        if Answer equal "stop" do:
            output "stopped"
            stop
        else do:
            output "again"
'''

    output = run_program(code, monkeypatch, capsys, inputs=["hello", "stop"])

    assert output == ["again", "stopped"]


def test_e2e_struct_inheritence(monkeypatch, capsys):
    code ='''create Character with:
    Health is 100
    Name
    
create Enemy from Character with:
    Name is "Jeff"

define Play:
    output Name from Enemy
    output Health from Enemy
'''

    output = run_program(code, monkeypatch, capsys, slot=995)

    assert output == ["Jeff", "100"]

