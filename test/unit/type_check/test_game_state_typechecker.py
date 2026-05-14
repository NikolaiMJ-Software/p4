import pytest
from src.visitors.type_checker import TypeChecker
from src.ast.nodes import *
from src.errors import TypeError


def test_create_game_struct_is_allowed():
    node = CreateStruct("Game", [None, [
        CreateVariable("Health", IntLiteral(100)),
        CreateVariable("Class", StringLiteral("Warrior"))
    ]])

    result = TypeChecker().check_create_struct(node, False, False)

    assert result is None


def test_create_game_variable_fails():
    node = CreateVariable("Game", IntLiteral(10))

    with pytest.raises(TypeError, match="reserved"):
        TypeChecker().check_create_variable(node, False)


def test_create_game_list_fails():
    node = CreateList("Game", [IntLiteral(1), IntLiteral(2)])

    with pytest.raises(TypeError, match="reserved"):
        TypeChecker().check_create_list(node, False)


def test_define_game_function_fails():
    node = Define("Game", [], [])

    with pytest.raises(TypeError, match="reserved"):
        TypeChecker().check_define(node, False)


def test_game_struct_can_contain_unassigned_fields():
    node = CreateStruct("Game", [None, [
        CreateVariable("Class", None),
        CreateVariable("Health", None)
    ]])

    result = TypeChecker().check_create_struct(node, False, False)

    assert result is None


def test_game_struct_field_can_be_assigned():
    node = Assign("Health", "Game", IntLiteral(80))

    game = {"Health": "int"}

    result = TypeChecker().check_assign(node, game)

    assert result is None


def test_assign_missing_game_field_fails():
    node = Assign("Class", "Game", StringLiteral("Warrior"))

    game = {"Health": "int"}

    with pytest.raises(TypeError, match="does not exist in the struct"):
        TypeChecker().check_assign(node, game)


def test_assign_game_field_fails_if_game_does_not_exist():
    node = Assign("Health", "Game", IntLiteral(80))

    with pytest.raises(TypeError, match="does not exist"):
        TypeChecker().check_assign(node, False)


def test_read_game_field_returns_type():
    node = Var("Health", "Game")

    game = {"Health": "int"}

    result = TypeChecker().check_var(node, game)

    assert result is None


def test_read_missing_game_field_fails():
    node = Var("Class", "Game")

    game = {"Health": "int"}

    with pytest.raises(TypeError, match="not defined in the struct"):
        TypeChecker().check_var(node, game)