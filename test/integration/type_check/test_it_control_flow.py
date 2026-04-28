import pytest
from src.visitors.type_checker import *
from src.ast.nodes import *
from setup_type_checker import type_check_test

'''
-----------------
Passing integration tests for control flow
-----------------
'''

def test_it_pass_if_valid():
    result = type_check_test(if_valid_code)
    assert [None] == result
if_valid_code = """if true do:
    create X is 1
else if false do:
    create Y is 2
else do:
    create Z is 3
"""


def test_it_pass_if_can_use_outer_variable():
    result = type_check_test(if_can_use_outer_variable_code)
    assert ["int", None] == result
if_can_use_outer_variable_code = """create X is 5
if true do:
    X
"""


def test_it_pass_else_can_use_outer_variable():
    result = type_check_test(else_can_use_outer_variable_code)
    assert ["int", None] == result
else_can_use_outer_variable_code = """create X is 5
if false do:
    create Y is 1
else do:
    X
"""


def test_it_pass_if_updates_outer_variable_type():
    result = type_check_test(if_updates_outer_variable_type_code)
    assert ["int", None, "float"] == result
if_updates_outer_variable_type_code = """create X is 5
if true do:
    X is 1.5
X
"""


def test_it_pass_if_else_updates_parent_variable_to_string():
    result = type_check_test(if_else_updates_parent_variable_to_string_code)
    assert ["int", None, "float"] == result
if_else_updates_parent_variable_to_string_code = """create X is 5
if true do:
    X is "h"
else do:
    X is 5.5
create Y is X
"""


def test_it_pass_if_else_updates_parent_variable_to_float():
    result = type_check_test(if_else_updates_parent_variable_to_float_code)
    assert ["int", None, "float"] == result
if_else_updates_parent_variable_to_float_code = """create X is 5
if false do:
    X is "h"
else do:
    X is 5.5
create Y is X
"""


def test_it_pass_else_updates_outer_variable_type():
    result = type_check_test(else_updates_outer_variable_type_code)
    assert ["int", None, "float"] == result
else_updates_outer_variable_type_code = """create X is 5
if false do:
    create Y is 1
else do:
    X is 1.5
X
"""


def test_it_pass_if_none_condition_skips_body():
    result = type_check_test(if_none_condition_skips_body_code)
    assert [None, None] == result
if_none_condition_skips_body_code = """create Cond
if Cond do:
    create X is 1
"""


def test_it_pass_while_valid_and_scope_restored():
    result = type_check_test(while_valid_code)
    assert ["bool", None] == result
while_valid_code = """create Cond is true
while Cond do:
    create X is 1
"""


def test_it_pass_dowhile_valid_and_scope_restored():
    result = type_check_test(dowhile_valid_code)
    assert ["bool", None] == result
dowhile_valid_code = """create Cond is true
do:
    create X is 1
while Cond
"""


def test_it_pass_if_with_expression_condition():
    result = type_check_test(if_expression_condition_code)
    assert [None] == result
if_expression_condition_code = """if 1 less than 2 do:
    create X is 1
"""


def test_it_pass_while_with_boolean_expression():
    result = type_check_test(while_boolean_expression_code)
    assert [None] == result
while_boolean_expression_code = """while true and false do:
    create X is 1
"""

def test_it_pass_dowhile_use_and_change_global_var_in_body():
    result = type_check_test(dowhile_global_var_code)
    assert ['int', None, 'float'] == result
dowhile_global_var_code = """create Y is 5
do:
    create X is 1
    Y is Y - X
    if Y equal 3 do:
        Y is 2.5
while Y greater than 2
create Z is Y
"""

def test_it_pass_while_use_and_change_global_var_in_body():
    result = type_check_test(while_global_var_code)
    assert ['int', None, 'float'] == result
while_global_var_code = """create Y is 5
while Y greater than 2 do:
    create X is 1
    Y is Y - X
    if Y equal 3 do:
        Y is 2.5
create Z is Y
"""

'''
-----------------
Failing integration tests for control flow
-----------------
'''

def test_it_fail_if_created_variable_does_not_leak():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(if_created_variable_does_not_leak_code)
    assert "does not exist" in str(exc_info.value)
if_created_variable_does_not_leak_code = """if true do:
    create X is 1
X
"""


def test_it_fail_else_created_variable_does_not_leak():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(else_created_variable_does_not_leak_code)
    assert "does not exist" in str(exc_info.value)
else_created_variable_does_not_leak_code = """if false do:
    create X is 1
else do:
    create Y is 2
Y
"""


def test_it_fail_if_invalid_condition():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(if_invalid_condition_code)
    assert "if condition must be bool, got int" in str(exc_info.value)
if_invalid_condition_code = """if 1 do:
    create X is 1
"""


def test_it_fail_if_invalid_elif_condition():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(if_invalid_elif_condition_code)
    assert "elif condition must be bool, got int" in str(exc_info.value)
if_invalid_elif_condition_code = """if true do:
    create X is 1
else if 1 do:
    create Y is 2
"""


def test_it_fail_while_invalid_condition():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(while_invalid_condition_code)
    assert "while condition must be bool, got int" in str(exc_info.value)
while_invalid_condition_code = """create Cond is 1
while Cond do:
    create X is 1
"""


def test_it_fail_dowhile_invalid_condition():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(dowhile_invalid_condition_code)
    assert "dowhile condition must be bool, got int" in str(exc_info.value)
dowhile_invalid_condition_code = """create Cond is 1
do:
    create X is 1
while Cond
"""


def test_it_fail_if_body_uses_invalid_operation():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(if_body_invalid_operation_code)
    assert "Expected numeric types" in str(exc_info.value)
if_body_invalid_operation_code = '''if true do:
    create X is "a" + 1
'''


def test_it_fail_if_else_parent_variable_conflicting_type_used_in_add():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(if_else_parent_variable_conflicting_type_used_in_add_code)
    assert "Expected numeric types" in str(exc_info.value)

if_else_parent_variable_conflicting_type_used_in_add_code = '''create Y is 5
create Z is 0
create X is chance 50%
if X do:
    Z is 69
else do:
    Z is "hej"
create T is Y + Z
'''