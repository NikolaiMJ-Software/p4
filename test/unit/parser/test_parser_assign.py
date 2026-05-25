import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

import pytest
from src.parser import parse, ParseError


####################
# assign functions #
####################

def test_assign():
    tree_int = parse("X is 5\n")
    tree_float = parse("X is 5.5\n")
    tree_string = parse("X is \"pop\"\n")
    tree_ID = parse("X is Y\n")
    tree_list = parse("X is listing: 1, 3, 2, 4\n")

    
    assert tree_int.children[0].data == "assign_stmt"
    assert tree_float.children[0].data == "assign_stmt"
    assert tree_string.children[0].data == "assign_stmt"
    assert tree_ID.children[0].data == "assign_stmt"
    assert tree_list.children[0].data == "assign_stmt"
    
def test_struct_attribute_assign():
    tree = parse("Health from Zombie is between 5 and 10\n")
    tree_assign_struct_list = parse("Health from Zombie is listing: \"a\", \"b\"\n")
    
    assert tree.children[0].data == "assign_stmt"
    assert tree_assign_struct_list.children[0].data == "assign_stmt"

def test_assign_index_value():
    tree_int = parse("index 0 of X is 5\n")
    tree_expr1 = parse("index 1+1 of X is 5\n")
    tree_expr2 = parse("index I of X is 5\n")
    tree_assign_index_ID = parse("index 1 of Y is 5\n")
    tree_assign_index_index_ID = parse("index 1 of index 3 of Y is 5\n")

    assert tree_int.children[0].data == "assign_index"
    assert tree_expr1.children[0].data == "assign_index"
    assert tree_expr2.children[0].data == "assign_index"
    assert tree_assign_index_ID.children[0].data == "assign_index"
    assert tree_assign_index_index_ID.children[0].data == "assign_index"

def test_assign_ID_index_value():
    tree_assign_ID_index = parse("X is index 1 of Y\n")
    tree_assign_ID_index_of_index = parse("X is index 1 of index 3 of Y\n")

    assert tree_assign_ID_index.children[0].data == "assign_stmt"
    assert tree_assign_ID_index_of_index.children[0].data == "assign_stmt"

def test_assign_index_from_struct_list():
    tree = parse("index 0 of Inventory from Player is \"Sword\"\n")
    node = tree.children[0]

    assert node.data == "assign_index"


def test_nested_index_access_expr():
    tree = parse("X is index 1 of index 3 of Y\n")
    node = tree.children[0]

    assert node.data == "assign_stmt"

def test_struct_field_access_expr():
    tree = parse("create X is Health from Zombie\n")
    node = tree.children[0]

    assert node.data == "create_v"
    assert node.children[0] == "X"


def test_assign_from_struct_field_expr():
    tree = parse("X is Health from Zombie + 5\n")
    node = tree.children[0]

    assert node.data == "assign_stmt"

