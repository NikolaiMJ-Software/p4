import builtins
import pytest

from src.ast import builder
from src.parser import parse
from src.visitors.interpreter import InterpreterVisitor
from src.errors import TypeError as TypeCheckError


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

def test_e2e_function_arguments_keep_runtime_types(monkeypatch, capsys):
    code = '''define AddNumbers with Y, V:
    return Y + V

create Number1 is 10
create Number2 is 25

define Play:
    output Number1 + Number2
    output call AddNumbers with Number1, Number2
'''

    output = run_program(code, monkeypatch, capsys, slot=994)

    assert output == ["35", "35"]


def test_e2e_simple_game_flow(monkeypatch, capsys):
    code = '''create Game with:
    Class
    Weapon
    Weapon_damage

create Class

define Play:
    output "Choose class"
    input in Class
    if Class equal "warrior" do:
        Class from Game is "Warrior"
        Weapon from Game is "sword"
        Weapon_damage from Game is 10
        output "Your class is:", Class from Game
        output "Your weapon is:", Weapon from Game
    else do:
        output "Invalid class"
'''

    output = run_program(code, monkeypatch, capsys, inputs=["warrior"], slot=993)

    assert output == [
        "Choose class",
        "Your class is: Warrior",
        "Your weapon is: sword"
    ]

def test_e2e_type_error_is_raised(monkeypatch, capsys):
    code = '''create Number is 10

define Play:
    output Number + "text"
'''

    with pytest.raises(TypeCheckError):
        run_program(code, monkeypatch, capsys, slot=992)


def test_e2e_type_error_does_not_save_broken_game_state(monkeypatch, capsys):
    slot = 991

    first_code = '''create Game with:
    Name

define Play:
    Name from Game is "Bob"
    output "saved"
'''

    output = run_program(first_code, monkeypatch, capsys, slot=slot)
    assert output == ["saved"]

    broken_code = '''create Game with:
    Name

define Play:
    Name from Game is "Alice"
    output MissingVariable
'''

    with pytest.raises(TypeCheckError):
        run_program(broken_code, monkeypatch, capsys, slot=slot)

    third_code = '''create Game with:
    Name

define Play:
    output Name from Game
'''

    output = run_program(third_code, monkeypatch, capsys, slot=slot)
    assert output == ["Bob"]


def test_e2e_list_index_output(monkeypatch, capsys):
    code = '''create Items is listing: "sword", "shield", "potion"

define Play:
    output index 0 of Items
    output index 2 of Items
'''

    output = run_program(code, monkeypatch, capsys, slot=990)

    assert output == ["sword", "potion"]


def test_e2e_list_index_assignment(monkeypatch, capsys):
    code = '''create Items is listing: "sword", "shield", "potion"

define Play:
    index 1 of Items is "axe"
    output index 1 of Items
'''

    output = run_program(code, monkeypatch, capsys, slot=989)

    assert output == ["axe"]


def test_e2e_for_range_loop(monkeypatch, capsys):
    code = '''define Play:
    for each I from 1 to 3 do:
        output I
'''

    output = run_program(code, monkeypatch, capsys, slot=988)

    assert output == ["1", "2", "3"]


def test_e2e_foreach_loop(monkeypatch, capsys):
    code = '''create Items is listing: "sword", "shield", "potion"

define Play:
    for each Item in Items do:
        output Item
'''

    output = run_program(code, monkeypatch, capsys, slot=987)

    assert output == ["sword", "shield", "potion"]


def test_e2e_function_return_value(monkeypatch, capsys):
    code = '''define AddNumbers with A, B:
    return A + B

define Play:
    output call AddNumbers with 10, 25
'''

    output = run_program(code, monkeypatch, capsys, slot=986)

    assert output == ["35"]



def test_e2e_string_concatenation(monkeypatch, capsys):
    code = '''create First is "Hello "
create Second is "World"

define Play:
    output First + Second
'''

    output = run_program(code, monkeypatch, capsys, slot=985)

    assert output == ["Hello World"]


def test_e2e_else_if_branch(monkeypatch, capsys):
    code = '''create Answer

define Play:
    input in Answer
    if Answer equal "yes" do:
        output "yes branch"
    else if Answer equal "maybe" do:
        output "maybe branch"
    else do:
        output "else branch"
'''

    output = run_program(code, monkeypatch, capsys, inputs=["maybe"], slot=984)

    assert output == ["maybe branch"]


def test_e2e_type_error_for_bad_arithmetic(monkeypatch, capsys):
    code = '''create Number is 10
create Text is "hello"

define Play:
    output Number + Text
'''

    with pytest.raises(TypeCheckError):
        run_program(code, monkeypatch, capsys, slot=983)


def test_e2e_type_error_for_non_int_index(monkeypatch, capsys):
    code = '''create Items is listing: "sword", "shield"

define Play:
    output index "zero" of Items
'''

    with pytest.raises(TypeCheckError):
        run_program(code, monkeypatch, capsys, slot=982)


def test_e2e_type_error_for_wrong_function_arg_count(monkeypatch, capsys):
    code = '''define AddNumbers with A, B:
    return A + B

define Play:
    call AddNumbers with 10
'''

    with pytest.raises(TypeCheckError):
        run_program(code, monkeypatch, capsys, slot=981)


def test_e2e_between_can_assign_numeric_value(monkeypatch, capsys):
    code = '''create Health

define Play:
    Health is between 1 and 1
    output Health
'''

    output = run_program(code, monkeypatch, capsys, slot=980)

    assert output == ["1"]


def test_e2e_chance_returns_bool(monkeypatch, capsys):
    code = '''create CriticalHit

define Play:
    CriticalHit is chance 1 in 1
    if CriticalHit do:
        output "critical"
    else do:
        output "normal"
'''

    output = run_program(code, monkeypatch, capsys, slot=978)

    assert output == ["critical"]


def test_e2e_do_while_runs_before_condition(monkeypatch, capsys):
    code = '''create X is 0

define Play:
    do:
        output "ran"
    while false
'''

    output = run_program(code, monkeypatch, capsys, slot=977)

    assert output == ["ran"]


def test_e2e_unary_negative_number(monkeypatch, capsys):
    code = '''create X is -5

define Play:
    output X
'''

    output = run_program(code, monkeypatch, capsys, slot=976)

    assert output == ["-5"]


def test_e2e_nested_struct_list_access(monkeypatch, capsys):
    code = '''create Player with:
    Items is listing: "sword", "shield"

define Play:
    output index 0 of Items from Player
'''

    output = run_program(code, monkeypatch, capsys, slot=975)

    assert output == ["sword"]