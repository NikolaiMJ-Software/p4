import pytest
from src.visitors.type_checker import TypeChecker
from src.ast.nodes import *
from src.errors import TypeError


def test_define_function():
    node = Define("Fun1", ["a", "b"], [])

    result = TypeChecker().check_define(node, False)

    assert result is None


def test_define_duplicate_function_fails():
    node = Define("Fun1", [], [])

    with pytest.raises(TypeError, match="already exist"):
        TypeChecker().check_define(node, True)


def test_call_missing_function_fails():
    node = Call("Fun1", [])

    with pytest.raises(TypeError, match="does not exist"):
        TypeChecker().check_call(node, False)


def test_call_too_few_args_fails():
    node = Call("Fun", [IntLiteral(1)])
    function = {
        "params": ["a", "b"],
        "body": []
    }

    with pytest.raises(TypeError, match="expects 2 args, got 1"):
        TypeChecker().check_call(node, function)


def test_call_too_many_args_fails():
    node = Call("Fun", [IntLiteral(1), IntLiteral(2)])
    function = {
        "params": ["a"],
        "body": []
    }

    with pytest.raises(TypeError, match="expects 1 args, got 2"):
        TypeChecker().check_call(node, function)


def test_call_correct_arg_count():
    node = Call("Fun", [IntLiteral(1), IntLiteral(2)])
    function = {
        "params": ["a", "b"],
        "body": []
    }

    result = TypeChecker().check_call(node, function)

    assert result is None


def test_define_function_without_params():
    node = Define("Fun0", [], [])

    result = TypeChecker().check_define(node, False)

    assert result is None


def test_call_zero_arg_function():
    node = Call("Fun0", [])
    function = {
        "params": [],
        "body": []
    }

    result = TypeChecker().check_call(node, function)

    assert result is None


def test_call_zero_arg_function_with_arg_fails():
    node = Call("Fun0", [IntLiteral(1)])
    function = {
        "params": [],
        "body": []
    }

    with pytest.raises(TypeError, match="expects 0 args, got 1"):
        TypeChecker().check_call(node, function)