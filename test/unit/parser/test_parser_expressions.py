import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

import pytest
from src.parser import parse, ParseError


###############
# Expressions #
###############

def test_math_expression():
    tree_add = parse("create X is 5+1\n")
    tree_pow = parse("create X is 5^1\n")
    tree_div = parse("create X is 5/1\n")
    tree_mul = parse("create X is 5*1\n")
    tree_sub_neg = parse("create X is 5-1\n")
    
    
    assert tree_add is not None
    assert tree_pow is not None
    assert tree_div is not None
    assert tree_mul is not None
    assert tree_sub_neg is not None

def test_boolean_expression():
    tree_and = parse("create X is true and false\n")
    tree_or = parse("create X is true or false\n")
    tree_not = parse("create X is not true\n")
    tree_equal = parse("create X is A equal Y\n")
    tree_greater = parse("create X is A greater than or equal to Y\n")
    tree_lesser = parse("create X is A less than or equal to Y\n")
    
    assert tree_and is not None
    assert tree_or is not None
    assert tree_not is not None
    assert tree_equal is not None
    assert tree_greater is not None
    assert tree_lesser is not None

def test_either_expression():
    tree = parse("create X is either true or false\n")
    assert tree is not None

def test_between_expression():
    tree = parse("create X is between 1 and 100\n")
    assert tree is not None
    
def test_chance_expression():
    tree_chance_1 = parse("create X is chance 30%\n")
    tree_chance_2 = parse("create X is chance 1 in 100\n")
    assert tree_chance_1 is not None
    assert tree_chance_2 is not None

def test_math_precedence_mul_before_add():
    tree = parse("create X is 1 + 2 * 3\n")
    expr = tree.children[0].children[1].children[0]

    assert expr.data == "add"
    assert expr.children[1].data == "mul"


def test_math_parentheses_override_precedence():
    tree = parse("create X is (1 + 2) * 3\n")
    expr = tree.children[0].children[1].children[0]

    assert expr.data == "mul"
    assert expr.children[0].data == "add"


def test_pow_right_associative():
    tree = parse("create X is 2^3^4\n")
    expr = tree.children[0].children[1].children[0]

    assert expr.data == "pow"
    assert expr.children[1].data == "pow"


def test_boolean_precedence_and_before_or():
    tree = parse("create X is true or false and true\n")
    expr = tree.children[0].children[1].children[0]

    assert expr.data == "or_expr"
    assert expr.children[1].data == "and_expr"


def test_comparison_inside_boolean_expression():
    tree = parse("create X is A equal B or C equal D\n")
    expr = tree.children[0].children[1].children[0]

    assert expr.data == "or_expr"
    assert expr.children[0].data == "equal_expr"
    assert expr.children[1].data == "equal_expr"
