import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

import pytest
from src.parser import parse, ParseError

############
# Comments #
############

def test_single_line_comment():
    code = """# comment
create X is 5
"""
    tree = parse(code)
    assert tree is not None


def test_block_comment():
    code = """#/
this is a comment
/#
create X is 5
"""
    tree = parse(code)
    assert tree is not None

