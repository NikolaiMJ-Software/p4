import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import pytest
from lark import UnexpectedInput
from parser import parse

# CREATE

def test_create_variable():
    tree = parse("create X is 5\n")
    assert tree.children[0].data == "create_v"
    