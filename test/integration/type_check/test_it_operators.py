import pytest
from src.visitors.type_checker import *
from src.ast.nodes import *
from setup_type_checker import type_check_test

'''
-----------------
Passing integration tests for operators
-----------------
'''

def test_it_pass_int_literal():
    result = type_check_test(int_literal_code)
    assert ["int"] == result
int_literal_code = """2
"""


def test_it_pass_float_literal():
    result = type_check_test(float_literal_code)
    assert ["float"] == result
float_literal_code = """2.5
"""


def test_it_pass_string_literal():
    result = type_check_test(string_literal_code)
    assert ["str"] == result
string_literal_code = '''"hello"
'''


def test_it_pass_bool_literal():
    result = type_check_test(bool_literal_code)
    assert ["bool"] == result
bool_literal_code = """true
"""


def test_it_pass_add_int_int():
    result = type_check_test(add_int_int_code)
    assert ["int"] == result
add_int_int_code = """2 + 2
"""


def test_it_pass_add_int_float():
    result = type_check_test(add_int_float_code)
    assert ["float"] == result
add_int_float_code = """2 + 2.0
"""


def test_it_pass_add_float_int():
    result = type_check_test(add_float_int_code)
    assert ["float"] == result
add_float_int_code = """2.0 + 2
"""


def test_it_pass_add_string_string():
    result = type_check_test(add_string_string_code)
    assert ["str"] == result
add_string_string_code = '''"a" + "b"
'''


def test_it_pass_mul_int_int():
    result = type_check_test(mul_int_int_code)
    assert ["int"] == result
mul_int_int_code = """2 * 2
"""


def test_it_pass_mul_int_float():
    result = type_check_test(mul_int_float_code)
    assert ["float"] == result
mul_int_float_code = """2 * 2.0
"""


def test_it_pass_div_int_int():
    result = type_check_test(div_int_int_code)
    assert ["float"] == result
div_int_int_code = """4 / 2
"""


def test_it_pass_pow_int_int():
    result = type_check_test(pow_int_int_code)
    assert ["int"] == result
pow_int_int_code = """2 ^ 3
"""


def test_it_pass_pow_int_float():
    result = type_check_test(pow_int_float_code)
    assert ["float"] == result
pow_int_float_code = """2 ^ 3.0
"""


def test_it_pass_equal_int_int():
    result = type_check_test(equal_int_int_code)
    assert ["bool"] == result
equal_int_int_code = """1 equal 1
"""


def test_it_pass_equal_int_float():
    result = type_check_test(equal_int_float_code)
    assert ["bool"] == result
equal_int_float_code = """1 equal 1.0
"""


def test_it_pass_equal_string_string():
    result = type_check_test(equal_string_string_code)
    assert ["bool"] == result
equal_string_string_code = '''"a" equal "b"
'''


def test_it_pass_not_equal_int_float():
    result = type_check_test(not_equal_int_float_code)
    assert ["bool"] == result
not_equal_int_float_code = """1 not equal 1.0
"""


def test_it_pass_greater_expr():
    result = type_check_test(greater_expr_code)
    assert ["bool"] == result
greater_expr_code = """2 greater than 1
"""


def test_it_pass_less_expr():
    result = type_check_test(less_expr_code)
    assert ["bool"] == result
less_expr_code = """1 less than 2.0
"""


def test_it_pass_greater_equal_expr():
    result = type_check_test(greater_equal_expr_code)
    assert ["bool"] == result
greater_equal_expr_code = """2.0 greater than or equal to 2
"""


def test_it_pass_less_equal_expr():
    result = type_check_test(less_equal_expr_code)
    assert ["bool"] == result
less_equal_expr_code = """2 less than or equal to 2.0
"""


def test_it_pass_and_expr():
    result = type_check_test(and_expr_code)
    assert ["bool"] == result
and_expr_code = """true and false
"""


def test_it_pass_or_expr():
    result = type_check_test(or_expr_code)
    assert ["bool"] == result
or_expr_code = """true or false
"""


def test_it_pass_not_expr():
    result = type_check_test(not_expr_code)
    assert ["bool"] == result
not_expr_code = """not true
"""


def test_it_pass_xor_expr():
    result = type_check_test(xor_expr_code)
    assert ["bool"] == result
xor_expr_code = """either true or false
"""


def test_it_pass_between_int_int():
    result = type_check_test(between_int_int_code)
    assert ["bool"] == result
between_int_int_code = """between 1 and 10
"""


def test_it_pass_between_float_int():
    result = type_check_test(between_float_int_code)
    assert ["bool"] == result
between_float_int_code = """between 1.5 and 10
"""


def test_it_pass_chance_percent():
    result = type_check_test(chance_percent_code)
    assert ["bool"] == result
chance_percent_code = """chance 30%
"""


def test_it_pass_chance_in():
    result = type_check_test(chance_in_code)
    assert ["bool"] == result
chance_in_code = """chance 30 in 100
"""


def test_it_pass_operator_in_variable_creation():
    result = type_check_test(operator_in_variable_creation_code)
    assert ["float"] == result
operator_in_variable_creation_code = """create X is 2 + 2.0
"""


def test_it_pass_comparison_in_if():
    result = type_check_test(comparison_in_if_code)
    assert [None] == result
comparison_in_if_code = """if 2 greater than 1 do:
    create X is 5
"""


def test_it_pass_boolean_in_if():
    result = type_check_test(boolean_in_if_code)
    assert [None] == result
boolean_in_if_code = """if true and false do:
    create X is 5
"""


'''
-----------------
Failing integration tests for operators
-----------------
'''

def test_it_fail_add_string_int():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(add_string_int_code)
    assert "Expected numeric types" in str(exc_info.value)
add_string_int_code = '''"a" + 2
'''


def test_it_fail_mul_string_int():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(mul_string_int_code)
    assert "Expected numeric types" in str(exc_info.value)
mul_string_int_code = '''"a" * 2
'''


def test_it_fail_div_string_int():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(div_string_int_code)
    assert "Expected numeric types" in str(exc_info.value)
div_string_int_code = '''"a" / 2
'''


def test_it_fail_pow_string_int():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(pow_string_int_code)
    assert "Expected numeric types" in str(exc_info.value)
pow_string_int_code = '''"a" ^ 2
'''


def test_it_fail_equal_string_int():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(equal_string_int_code)
    assert "Cannot compare" in str(exc_info.value)
equal_string_int_code = '''"a" equal 1
'''


def test_it_fail_not_equal_string_bool():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(not_equal_string_bool_code)
    assert "Cannot compare" in str(exc_info.value)
not_equal_string_bool_code = '''"a" not equal true
'''


def test_it_fail_greater_string_int():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(greater_string_int_code)
    assert "Cannot compare" in str(exc_info.value)
greater_string_int_code = '''"a" greater than 1
'''


def test_it_fail_less_bool_int():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(less_bool_int_code)
    assert "Cannot compare" in str(exc_info.value)
less_bool_int_code = """true less than 1
"""


def test_it_fail_and_int_bool():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(and_int_bool_code)
    assert "AND requires bool" in str(exc_info.value)
and_int_bool_code = """1 and false
"""


def test_it_fail_or_string_bool():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(or_string_bool_code)
    assert "OR requires bool" in str(exc_info.value)
or_string_bool_code = '''"a" or false
'''


def test_it_fail_not_int():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(not_int_code)
    assert "NOT requires bool" in str(exc_info.value)
not_int_code = """not 1
"""


def test_it_fail_xor_bool_int():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(xor_bool_int_code)
    assert "XOR requires bool" in str(exc_info.value)
xor_bool_int_code = """either true or 1
"""


def test_it_fail_between_string_int():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(between_string_int_code)
    assert "between requires numeric types" in str(exc_info.value)
between_string_int_code = '''between "a" and 10
'''


def test_it_fail_chance_bool_int():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(chance_bool_int_code)
    assert "chance requires numeric types" in str(exc_info.value)
chance_bool_int_code = """chance true in 100
"""