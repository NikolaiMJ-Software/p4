#Tester parser->builder->node
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.parser import parse
from src.ast.builder import ASTBuilder


def test_ast_create_var():
    tree = parse("create X is 5\n")
    ast = ASTBuilder().transform(tree)

    node = ast[0]

    assert node.__class__.__name__ == "Create_v"
    assert node.name == "X"
    assert node.value.value == 5

def test_ast_create_struct():
    code = """create X with:
    Health
    Speed
"""
    tree = parse(code)
    ast = ASTBuilder().transform(tree)

    node = ast[0]

    assert node.__class__.__name__ == "Create_s"
    assert node.name == "X"
    assert len(node.fields) == 2

def test_ast_assign():
    tree = parse("X is 5\n")
    ast = ASTBuilder().transform(tree)

    node = ast[0]

    assert node.__class__.__name__ == "Assign"
    assert node.name == "X"
    assert node.value.value == 5

def test_ast_add_expr():
    tree = parse("create X is 5+1\n")
    ast = ASTBuilder().transform(tree)

    node = ast[0]

    assert node.value.__class__.__name__ == "Add"
    assert node.value.left.value == 5
    assert node.value.right.value == 1

def test_ast_if():
    code = """if true do:
    X is 5
"""
    tree = parse(code)
    ast = ASTBuilder().transform(tree)

    node = ast[0]

    assert node.__class__.__name__ == "If"
    assert node.cond.value == True
    assert len(node.body) == 1

def test_ast_function():
    code = """define X with A, B:
    return A
"""
    tree = parse(code)
    ast = ASTBuilder().transform(tree)

    node = ast[0]

    assert node.__class__.__name__ == "Define"
    assert node.name == "X"
    assert node.params == ["A", "B"]

def test_ast_call():
    tree = parse("call Func with 1, 2\n")
    ast = ASTBuilder().transform(tree)

    node = ast[0]

    assert node.value.__class__.__name__ == "Call"
    assert node.value.name == "Func"
    assert len(node.value.args) == 2

def test_ast_create_list():
    tree = parse("create X listing: 1, 2, 3\n")
    ast = ASTBuilder().transform(tree)

    node = ast[0]

    assert node.__class__.__name__ == "Create_l"
    assert len(node.listing) == 3
    assert node.listing[0].value == 1

def test_ast_between():
    tree = parse("create X is between 1 and 10\n")
    ast = ASTBuilder().transform(tree)

    node = ast[0]

    assert node.value.__class__.__name__ == "Between"

def test_ast_chance():
    tree = parse("create X is chance 30%\n")
    ast = ASTBuilder().transform(tree)

    node = ast[0]

    assert node.value.__class__.__name__ == "Chance"