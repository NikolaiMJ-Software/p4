#Tester parser->builder->node
#første pipeline test whuuuuuu!
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.parser import parse
from src.ast.builder import ASTBuilder


def test_ast_create_var():
    tree = parse("create X is 5\n")
    ast = ASTBuilder().transform(tree)

    node = ast[0]

    assert node.__class__.__name__ == "CreateVariable"
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

    assert node.__class__.__name__ == "CreateStruct"
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

    assert node.__class__.__name__ == "CreateList"
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
    
    
def test_ast_assign_list():
    tree = parse("X is listing: 1, 3, 2, 4\n")
    ast = ASTBuilder().transform(tree)

    node = ast[0]

    assert node.__class__.__name__ == "Assign"
    assert node.name == "X"
    assert node.base is None
    assert isinstance(node.value, list)
    assert [item.value for item in node.value] == [1, 3, 2, 4]


def test_ast_assign_struct_list():
    tree = parse('Health from Zombie is listing: "a", "b"\n')
    ast = ASTBuilder().transform(tree)

    node = ast[0]

    assert node.__class__.__name__ == "Assign"
    assert node.name == "Health"
    assert node.base == "Zombie"
    assert isinstance(node.value, list)
    assert [item.value for item in node.value] == ["a", "b"]


def test_ast_assign_index_value():
    tree = parse("X is index 1 of Y\n")
    ast = ASTBuilder().transform(tree)

    node = ast[0]

    assert node.__class__.__name__ == "Assign"
    assert node.name == "X"
    assert node.base is None

    assert node.value.__class__.__name__ == "IndexAccess"
    assert node.value.index.value == 1
    assert node.value.target.__class__.__name__ == "Var"
    assert node.value.target.name == "Y"
    assert node.value.target.base is None


def test_ast_assign_nested_index_value():
    tree = parse("X is index 1 of index 3 of Y\n")
    ast = ASTBuilder().transform(tree)

    node = ast[0]
    outer = node.value
    inner = outer.target

    assert node.__class__.__name__ == "Assign"
    assert node.name == "X"

    assert outer.__class__.__name__ == "IndexAccess"
    assert outer.index.value == 1

    assert inner.__class__.__name__ == "IndexAccess"
    assert inner.index.value == 3
    assert inner.target.__class__.__name__ == "Var"
    assert inner.target.name == "Y"


def test_ast_assign_to_index():
    tree = parse("index 1 of Y is 5\n")
    ast = ASTBuilder().transform(tree)

    node = ast[0]

    assert node.__class__.__name__ == "AssignIndex"
    assert node.target.__class__.__name__ == "IndexAccess"
    assert node.target.index.value == 1
    assert node.target.target.__class__.__name__ == "Var"
    assert node.target.target.name == "Y"
    assert node.value.value == 5


def test_ast_assign_to_nested_index():
    tree = parse('index 2 of index 1 of Y is "goat"\n')
    ast = ASTBuilder().transform(tree)

    node = ast[0]
    outer = node.target
    inner = outer.target

    assert node.__class__.__name__ == "AssignIndex"
    assert node.value.__class__.__name__ == "StringLiteral"
    assert node.value.value == "goat"

    assert outer.__class__.__name__ == "IndexAccess"
    assert outer.index.value == 2

    assert inner.__class__.__name__ == "IndexAccess"
    assert inner.index.value == 1
    assert inner.target.__class__.__name__ == "Var"
    assert inner.target.name == "Y"


def test_ast_output_expr_list():
    tree = parse('output "hello", X, 5\n')
    ast = ASTBuilder().transform(tree)

    node = ast[0]

    assert node.__class__.__name__ == "Output"
    assert isinstance(node.value, list)
    assert len(node.value) == 3
    assert node.value[0].__class__.__name__ == "StringLiteral"
    assert node.value[0].value == "hello"
    assert node.value[1].__class__.__name__ == "Var"
    assert node.value[1].name == "X"
    assert node.value[2].__class__.__name__ == "IntLiteral"
    assert node.value[2].value == 5