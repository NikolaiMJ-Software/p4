import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

import pytest
from lark import UnexpectedInput
from parser import parse


####Expand the test to include values within to see if they also fits and are right######

####################
# CREATE functions #
####################
# Variabels
def test_create_variable_assigned():
    tree_int = parse("create X is 5\n")
    tree_string = parse("create X is \"cake\"\n")
    tree_float = parse("create X is 5.5\n")
    tree_cond = parse("create X is 5 or 6\n")
    
    assert tree_int.children[0].data == "create_v"
    assert tree_string.children[0].data == "create_v"
    assert tree_float.children[0].data == "create_v"
    assert tree_cond.children[0].data == "create_v"
    
def test_create_variable_unassigned():
    tree = parse("create X\n")
    assert tree.children[0].data == "create_v"

#Lists
def test_create_list():
    tree_int = parse("create X listing: 1, 2, 3\n")
    tree_string = parse("create X listing: \"a\", \"b\", \"c\"\n")
    tree_float = parse("create X listing: 1.2, 3, 2.11\n")
    tree_ID = parse("create X listing: A, B, C\n")
    
    assert tree_int.children[0].data == "create_l"
    assert tree_string.children[0].data == "create_l"
    assert tree_float.children[0].data == "create_l"
    assert tree_ID.children[0].data == "create_l"

#Stucts
def test_creat_struct():
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
    
    code_test = """create X from Y"""
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

####################
# assign functions #
####################

def test_assign():
    tree_int = parse("X is 5\n")
    tree_float = parse("X is 5.5\n")
    tree_string = parse("X is \"pop\"\n")
    tree_ID = parse("X is Y\n")
    tree_list = parse("X is listing: 1, 3, 2, 4\n")

    
    assert tree_int.children[0].data == "assign_v"
    assert tree_float.children[0].data == "assign_v"
    assert tree_string.children[0].data == "assign_v"
    assert tree_ID.children[0].data == "assign_v"
    assert tree_list.children[0].data == "assign_l"
    
def test_struct_attribute_assign():
    tree = parse("Health from Zombie is between 5 and 10\n")
    tree_assign_struct_list = parse("Health from Zombie is listing: \"a\", \"b\"\n")
    
    assert tree.children[0].data == "assign_v"
    assert tree_assign_struct_list.children[0].data == "assign_l"

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

    assert tree_assign_ID_index.children[0].data == "assign_i"
    assert tree_assign_ID_index_of_index.children[0].data == "assign_i"

################
# Control Flow #
################

def test_if_stmt():
    code = """if true do:
    X is 5
    create Y
    output Y, X, "cake"
    """
    
    tree = parse(code)
    
    assert tree.children[0].data == "if_stmt"

def test_if_else_stmt():
    code = """if true do:
    X is 5
    create Y
    output Y
else do:
    output 0
    """
    
    tree = parse(code)
    
    assert tree.children[0].data == "if_stmt"

def test_if_elif_else():
    code = """if true do:
    output 1
else if false do:
    output 2
else do:
    output 3
"""
    tree = parse(code)
    assert tree.children[0].data == "if_stmt"


def test_while_loop():
    code ="""while true do:
    X is X+1
    """
    tree = parse(code)

    assert tree.children[0].data == "while_stmt"

def test_do_while():
    code = """do:
    Y is Y-1
while true

"""
    
    tree = parse(code)
    
    assert tree.children[0].data == "dowhile_stmt"

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
    assert node.children[0] == "X"
    assert node.children[1].value == "1"
    assert node.children[2].value == "10"

    body = next(child for child in node.children if hasattr(child, "data") and child.data == "mul_stmt")
    assert len(body.children) == 1
    assert body.children[0].data == "assign_v"

def test_foreach():
    code="""for each X in Y do:
    Hate is X+Y
    
    """
    
    tree = parse(code)
    
    assert tree.children[0].data == "foreach_stmt"    

#############
# Functions #
#############

def test_define_function():
    code = """define X:
    return V
    
    """

    tree = parse(code)
    
    assert tree.children[0].data == "func_def"
    
def test_define_func_param():
    code = """define Y with A, B, C:
    X is A+B+C
    return X
    """
    tree = parse(code)
    
    assert tree.children[0].data == "func_def"


def test_call():
    tree = parse("call Function\n")
    assert tree.children[0].data == "expr_stmt"

def test_call_param():
    tree = parse("call Function with 1, 2\n")
    assert tree.children[0].data == "expr_stmt"

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
    assert stmts[1].data == "assign_v"
    
    
    
def test_struct_with_comments():
    code = """create X with:
    A is 5
    
    # comment
    
    B is 10
"""
    tree = parse(code)
    assert tree is not None
    
def test_break_stmt():
    tree = parse("stop\n")
    assert tree.children[0].data == "break_stmt"
##################
# Negative tests #
##################

def test_create_missing_id():
    with pytest.raises(UnexpectedInput):
        parse("create is \"idk\"\n")

def test_create_lowercase_id():
    with pytest.raises(UnexpectedInput):
        parse("create x is 5\n")

def test_create_missing_expr():
    with pytest.raises(UnexpectedInput):
        parse("create X is\n")

def test_create_list_trailing_comma():
    with pytest.raises(UnexpectedInput):
        parse("create X listing: 1, 2, 3,\n")
        
def test_assign_missing_expr():
    with pytest.raises(UnexpectedInput):
        parse("X is\n")
        
def test_assign_lowercase_id():
    with pytest.raises(UnexpectedInput):
        parse("x is 5\n")

def test_struct_bad_indent():
    with pytest.raises(UnexpectedInput):
        parse("""create X with:
              Health
                Speed
              
              """)

def test_struct_lowercase_expr():
    with pytest.raises(UnexpectedInput):
        parse("""create X with:
              health
              
              """)
        
def test_else_stmt_missing_if():
    with pytest.raises(UnexpectedInput):
        parse("""else do:
              output 0
              """)
        
def test_if_stmt_missing_indent():
    with pytest.raises(UnexpectedInput):
        parse("""if true do:
            output 1
              """)
        
def test_while_stmt_missing_do():
    with pytest.raises(UnexpectedInput):
        parse("""while true:
              X is 5
              """)
        
def test_do_while_stmt_missing_while():
    with pytest.raises(UnexpectedInput):
        parse("""do:
              X is 5
              """)

def test_foreach_stmt_missing_in():
    with pytest.raises(UnexpectedInput):
        parse("""for each X Y do:
              X is 5
              """)

def test_define_missing_colon():
    with pytest.raises(UnexpectedInput):
        parse("""define X
              return Y
              """)

def test_input_missing_id():
    with pytest.raises(UnexpectedInput):
        parse("input in\n")


def test_output_missing_expr():
    with pytest.raises(UnexpectedInput):
        parse("output\n")


def test_equal_missing_lhs():
    with pytest.raises(UnexpectedInput):
        parse("create X is equal Y\n")


def test_between_missing_rhs():
    with pytest.raises(UnexpectedInput):
        parse("create X is between 1 and\n")


def test_chance_missing_value():
    with pytest.raises(UnexpectedInput):
        parse("create X is chance %\n")


def test_element_missing_array():
    with pytest.raises(UnexpectedInput):
        parse("element X in\n")


def test_unclosed_block_comment():
    with pytest.raises(UnexpectedInput):
        parse("""#/
this comment never closes
create X is 5
""")
        
def test_assign_index_not_allowed_value():
    with pytest.raises(UnexpectedInput):
        parse("index 1 of Y is 5 + 1\n")
        