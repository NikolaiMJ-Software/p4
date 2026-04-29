import pytest

from src.visitors.type_checker import TypeCheckerVisitor
from src.ast.nodes import *
from src.errors import TypeError


def make_checker():
    return TypeCheckerVisitor()


def game_struct(fields):
    return CreateStruct("Game", [None, fields])


def test_create_game_struct_is_allowed():
    checker = make_checker()

    node = game_struct([
        CreateVariable("Health", IntLiteral(100)),
        CreateVariable("Class", StringLiteral("Warrior"))
    ])

    assert checker.visit(node) is None
    assert "Game" in checker.v_table
    assert checker.v_table["Game"]["Health"] == "int"
    assert checker.v_table["Game"]["Class"] == "str"


def test_create_game_variable_fails():
    checker = make_checker()

    node = CreateVariable("Game", IntLiteral(10))

    with pytest.raises(TypeError, match="reserved"):
        checker.visit(node)


def test_create_game_list_fails():
    checker = make_checker()

    node = CreateList("Game", [IntLiteral(1), IntLiteral(2)])

    with pytest.raises(TypeError, match="reserved"):
        checker.visit(node)


def test_define_game_function_fails():
    checker = make_checker()

    node = Define("Game", [], [])

    with pytest.raises(TypeError, match="reserved"):
        checker.visit(node)


def test_game_struct_can_contain_unassigned_fields():
    checker = make_checker()

    node = game_struct([
        CreateVariable("Class", None),
        CreateVariable("Health", None)
    ])

    checker.visit(node)

    assert checker.v_table["Game"]["Class"] is None
    assert checker.v_table["Game"]["Health"] is None


def test_game_struct_field_can_be_assigned():
    checker = make_checker()

    checker.visit(
        game_struct([
            CreateVariable("Health", IntLiteral(100))
        ])
    )

    node = Assign("Health", "Game", IntLiteral(80))

    result = checker.visit(node)

    assert result == "int"
    assert checker.v_table["Game"]["Health"] == "int"


def test_assign_missing_game_field_fails():
    checker = make_checker()

    checker.visit(
        game_struct([
            CreateVariable("Health", IntLiteral(100))
        ])
    )

    node = Assign("Class", "Game", StringLiteral("Warrior"))

    with pytest.raises(TypeError, match="does not exist in the struct"):
        checker.visit(node)


def test_assign_game_field_fails_if_game_does_not_exist():
    checker = make_checker()

    node = Assign("Health", IntLiteral(80), "Game")

    with pytest.raises(TypeError, match="does not exist"):
        checker.visit(node)


def test_read_game_field_returns_type():
    checker = make_checker()

    checker.visit(
        game_struct([
            CreateVariable("Health", IntLiteral(100))
        ])
    )

    result = checker.visit(Var("Health", "Game"))

    assert result == "int"


def test_read_missing_game_field_fails():
    checker = make_checker()

    checker.visit(
        game_struct([
            CreateVariable("Health", IntLiteral(100))
        ])
    )

    with pytest.raises(TypeError, match="not defined in the struct"):
        checker.visit(Var("Class", "Game"))