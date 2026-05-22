import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

import pytest
from src.parser import parse, ParseError


##################
# Negative tests #
##################

def test_create_missing_id():
    with pytest.raises(ParseError):
        parse("create is \"idk\"\n")

def test_create_lowercase_id():
    with pytest.raises(ParseError):
        parse("create x is 5\n")

def test_create_missing_expr():
    with pytest.raises(ParseError):
        parse("create X is\n")

def test_create_list_trailing_comma():
    with pytest.raises(ParseError):
        parse("create X is listing: 1, 2, 3,\n")
        
def test_assign_missing_expr():
    with pytest.raises(ParseError):
        parse("X is\n")
        
def test_assign_lowercase_id():
    with pytest.raises(ParseError):
        parse("x is 5\n")

def test_struct_bad_indent():
    with pytest.raises(ParseError):
        parse("""create X with:
              Health
                Speed
              
              """)

def test_struct_lowercase_expr():
    with pytest.raises(ParseError):
        parse("""create X with:
              health
              
              """)
        
def test_else_stmt_missing_if():
    with pytest.raises(ParseError):
        parse("""else do:
              output 0
              """)
        
def test_if_stmt_missing_indent():
    with pytest.raises(ParseError):
        parse("""if true do:
            output 1
              """)
        
def test_while_stmt_missing_do():
    with pytest.raises(ParseError):
        parse("""while true:
              X is 5
              """)
        
def test_do_while_stmt_missing_while():
    with pytest.raises(ParseError):
        parse("""do:
              X is 5
              """)

def test_foreach_stmt_missing_in():
    with pytest.raises(ParseError):
        parse("""for each X Y do:
              X is 5
              """)

def test_define_missing_colon():
    with pytest.raises(ParseError):
        parse("""define X
              return Y
              """)

def test_input_missing_id():
    with pytest.raises(ParseError):
        parse("input in\n")


def test_output_missing_expr():
    with pytest.raises(ParseError):
        parse("output\n")


def test_equal_missing_lhs():
    with pytest.raises(ParseError):
        parse("create X is equal Y\n")


def test_between_missing_rhs():
    with pytest.raises(ParseError):
        parse("create X is between 1 and\n")


def test_chance_missing_value():
    with pytest.raises(ParseError):
        parse("create X is chance %\n")


def test_element_missing_array():
    with pytest.raises(ParseError):
        parse("element X in\n")


def test_unclosed_block_comment():
    with pytest.raises(ParseError):
        parse("""#/
this comment never closes
create X is 5
""")
        
def test_assign_index_allowed_value():
    parse("index 1 of Y is 5 + 1\n")


def test_index_missing_of():
    with pytest.raises(ParseError):
        parse("X is index 1 Y\n")


def test_index_missing_target():
    with pytest.raises(ParseError):
        parse("X is index 1 of\n")


def test_assign_index_missing_value():
    with pytest.raises(ParseError):
        parse("index 1 of X is\n")


def test_foreach_missing_array():
    with pytest.raises(ParseError):
        parse("""for each X in do:
    X is 5
""")


def test_call_missing_function_name():
    with pytest.raises(ParseError):
        parse("call with 1, 2\n")


def test_define_lowercase_name():
    with pytest.raises(ParseError):
        parse("""define test:
    return 1
""")


def test_function_param_lowercase():
    with pytest.raises(ParseError):
        parse("""define X with a:
    return a
""")
        