import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

import pytest
from src.parser import parse, ParseError


########
# MISC #
########

def test_blank_lines():
    code = """

create X


X is 5

"""
    tree = parse(code)

    # find rigtige statements
    stmts = [child for child in tree.children if hasattr(child, "data")]

    assert stmts[0].data == "create_v"
    assert stmts[1].data == "assign_stmt"
    
    
    
def test_struct_with_comments():
    code = """create X with:
    A is 5
    
    # comment
    
    B is 10
"""
    tree = parse(code)
    assert tree is not None
    
def test_break_stmt():
    code = """while true do:
    stop
    """
    tree = parse(code)
    assert tree.children[0].children[2].children[1].data == "break_stmt"
    
