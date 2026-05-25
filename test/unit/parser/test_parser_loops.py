import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

import pytest
from src.parser import parse, ParseError

#########
# Loops #
#########

def test_forrange():
    code = """for each X from 1 to 10 do:
    X is Cake+1
"""
    tree = parse(code)

    node = tree.children[0]

    assert node.data == "forrange_stmt"
    assert len([child for child in node.children if isinstance(child, str) and len(child) and " " not in child]) == 3
    assert node.children[0] == "X"
    assert node.children[1].value == "1"
    assert node.children[2].value == "10"

    body = next(child for child in node.children if hasattr(child, "data") and child.data == "block")
    assert len(body.children) == 3
    assert body.children[1].data == "assign_stmt"

def test_foreach():
    code="""for each X in Y do:
    Hate is X+Y
    
    """
    
    tree = parse(code)
    node = tree.children[0]
    
    assert node.data == "foreach_stmt"
    assert node.children[0] == "X"
    assert node.children[1] == "Y"

    body = next(child for child in node.children if hasattr(child, "data") and child.data == "block")
    assert len(body.children) == 5
    assert body.children[1].data == "assign_stmt"
    