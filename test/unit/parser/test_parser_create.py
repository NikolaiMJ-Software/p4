import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

import pytest
from src.parser import parse, ParseError



####################
# CREATE functions #
####################
# Variabels
def test_create_variable_assigned():
    tree_int = parse("create X is 5\n")
    tree_string = parse("create X is \"cake\"\n")
    tree_float = parse("create X is 5.5\n")
    tree_cond = parse("create X is 5 or 6\n")
    
    node_int = tree_int.children[0]
    assert node_int.data == "create_v"
    assert node_int.children[0] == "X"
    value_int = node_int.children[1].children[0]
    assert value_int.type == "INTEGER"
    assert value_int.value == "5"
    
    node_string = tree_string.children[0]
    assert node_string.data == "create_v"
    assert node_string.children[0] == "X"
    value_string = node_string.children[1].children[0]
    assert value_string.type == "STRING"
    assert value_string.value == '"cake"'
    
    node_float = tree_float.children[0]
    assert node_float.data == "create_v"
    assert node_float.children[0] == "X"
    value_float = node_float.children[1].children[0]
    assert value_float.type == "FLOAT"
    assert value_float.value == "5.5"
    
    node_cond = tree_cond.children[0]
    assert node_cond.data == "create_v"
    assert node_cond.children[0] == "X"
    value_cond = node_cond.children[1].children[0]
    assert value_cond.data == "or_expr"
    assert value_cond.children[0].type == "INTEGER"
    assert value_cond.children[0].value == "5"
    assert value_cond.children[1].type == "INTEGER"
    assert value_cond.children[1].value == "6"
    

def test_create_variable_unassigned():
    tree = parse("create X\n")
    
    node = tree.children[0]
    
    assert node.data == "create_v"
    assert node.children[0]=="X"

#Lists
def test_create_list():
    tree_int = parse("create X is listing: 1, 2, 3\n")
    tree_string = parse("create X is listing: \"a\", \"b\", \"c\"\n")
    tree_float = parse("create X is listing: 1.2, 3.1, 2.11\n")
    tree_ID = parse("create X is listing: A, B, C\n")
    
    node_int = tree_int.children[0]
    assert node_int.data == "create_l"
    assert node_int.children[0] == "X"
    list_tail = node_int.children[1]
    list_items = list_tail.children[0]
    first_item = list_items.children[0].children[0]
    second_item = list_items.children[1].children[0]
    third_item = list_items.children[2].children[0]
    assert first_item.type == "INTEGER"
    assert first_item.value == "1"
    assert second_item.type == "INTEGER"
    assert second_item.value == "2"
    assert third_item.type == "INTEGER"
    assert third_item.value == "3"
    
    node_string = tree_string.children[0]
    assert node_string.data == "create_l"
    assert node_string.children[0] == "X"
    list_tail = node_string.children[1]
    list_items = list_tail.children[0]
    first_item = list_items.children[0].children[0]
    second_item = list_items.children[1].children[0]
    third_item = list_items.children[2].children[0]
    assert first_item.type == "STRING"
    assert first_item.value == '"a"'
    assert second_item.type == "STRING"
    assert second_item.value == '"b"'
    assert third_item.type == "STRING"
    assert third_item.value == '"c"'
    
    node_float = tree_float.children[0]
    assert node_float.data == "create_l"
    assert node_float.children[0] == "X"
    list_tail = node_float.children[1]
    list_items = list_tail.children[0]
    first_item = list_items.children[0].children[0]
    second_item = list_items.children[1].children[0]
    third_item = list_items.children[2].children[0]
    assert first_item.type == "FLOAT"
    assert first_item.value == "1.2"
    assert second_item.type == "FLOAT"
    assert second_item.value == "3.1"
    assert third_item.type == "FLOAT"
    assert third_item.value == "2.11"
    
    node_ID = tree_ID.children[0]
    assert node_ID.data == "create_l"
    assert node_ID.children[0] == "X"
    list_tail = node_ID.children[1]
    list_items = list_tail.children[0]
    first_item = list_items.children[0].children[0]
    second_item = list_items.children[1].children[0]
    third_item = list_items.children[2].children[0]
    assert first_item.data == "var"
    assert first_item.children[0] == "A"
    assert second_item.data == "var"
    assert second_item.children[0] == "B"
    assert third_item.data == "var"
    assert third_item.children[0] == "C"

def test_create_empty_list():
    tree = parse("create X is listing:\n")
    node = tree.children[0]

    assert node.data == "create_l"
    assert node.children[0] == "X"


def test_create_nested_list():
    tree = parse("create X is listing: 1, listing: 2, 3\n")
    node = tree.children[0]

    assert node.data == "create_l"

#Stucts
def test_create_struct():
    code = """create X with:
    Health
    
    Speed
    
    """
    
    code_with_values = """create X with:
    Health is between 5 and 10
    Speed is chance 30%
    Coolness is chance 10 in 100
    Items is listing: 1, 2, 3, "cake"
    """
    
    code_comment = """create X with:
    #/ HEALTH is based on
        dreams
        caffine
        death
    /#
    Health
    #hello
    Speed #test
    """
    
    tree = parse(code)
    tree_value = parse(code_with_values)
    tree_comment = parse(code_comment)
    
    assert tree.children[0].data == "create_s"
    assert tree_value.children[0].data == "create_s"
    assert tree_comment.children[0].data == "create_s"

def test_creat_struct_inheritance():
    code="""create Y from X with:
    Cake
    Fun
    Fear
    """
    
    tree = parse(code)
    
    assert tree.children[0].data == "create_s"

def test_struct_empty_list_field():
    code = """create X with:
    Items is listing:
"""
    tree = parse(code)

    assert tree.children[0].data == "create_s"
