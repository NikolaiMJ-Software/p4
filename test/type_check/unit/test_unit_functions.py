import pytest
from src.visitors.type_checker import *
from src.ast.nodes import *

def make_checker():
    return TypeCheckerVisitor()


def test_define_function():
    checker = make_checker()

    node = Define(
        "Fun1",
        ["a", "b"],
        [Return(Add(Var("a", None), Var("b", None)))]
    )

    assert checker.visit(node) is None
    assert "Fun1" in checker.f_table


def test_define_duplicate_function_fails():
    checker = make_checker()

    node = Define("Fun1", [], [])
    checker.visit(node)

    with pytest.raises(TypeError, match="already exist"):
        checker.visit(node)


def test_call_missing_function_fails():
    checker = make_checker()

    with pytest.raises(TypeError, match="don't exist"):
        checker.visit(Call("Fun1", []))


def test_call_function_returns_type():
    checker = make_checker()

    checker.visit(
        Define(
            "Fun1",
            ["a", "b"],
            [Return(Add(Var("a", None), Var("b", None)))]
        )
    )

    result = checker.visit(Call("Fun1", [IntLiteral(1), FloatLiteral(2.0)]))
    assert result == "float"


def test_call_restores_scope():
    checker = make_checker()
    checker.v_table["outside"] = "str"

    checker.visit(
        Define(
            "Fun1",
            ["a"],
            [Return(Var("a", None))]
        )
    )

    checker.visit(Call("Fun1", [IntLiteral(1)]))

    assert checker.v_table["outside"] == "str"
    assert "a" not in checker.v_table


def test_define_function_without_params():
    checker = make_checker()

    node = Define(
        "Fun0",
        [],
        [Return(IntLiteral(1))]
    )

    assert checker.visit(node) is None
    assert "Fun0" in checker.f_table


def test_call_zero_arg_function_returns_type():
    checker = make_checker()

    checker.visit(
        Define(
            "Fun0",
            [],
            [Return(IntLiteral(1))]
        )
    )

    assert checker.visit(Call("Fun0", [])) == "int"


def test_call_function_without_return_returns_none():
    checker = make_checker()

    checker.visit(
        Define(
            "Fun1",
            ["a"],
            [CreateVariable("x", Var("a", None))]
        )
    )

    assert checker.visit(Call("Fun1", [IntLiteral(1)])) is None