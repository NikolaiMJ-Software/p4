import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

import pytest
from src.parser import parse, ParseError


#######
# I/O #
#######

def test_input():
    tree = parse("input in X\n")
    assert tree.children[0].data == "input_stmt"

def test_output():
    tree = parse("output \"goat\"\n")
    assert tree.children[0].data == "output_stmt"

def test_output_index():
    tree = parse("output index 2 of X\n")
    tree_index = parse("output index 2 of index 7 of index 10 of index I of X\n")
    
    assert tree.children[0].data == "output_stmt"
    assert tree_index.children[0].data == "output_stmt"
    
def test_input_index():
    tree = parse("input in index 0 of X\n")
    node = tree.children[0]

    assert node.data == "input_stmt"


def test_input_struct_field():
    tree = parse("input in Health from Zombie\n")
    node = tree.children[0]

    assert node.data == "input_stmt"


def test_input_index_struct_field():
    tree = parse("input in index 0 of Inventory from Player\n")
    node = tree.children[0]

    assert node.data == "input_stmt"

