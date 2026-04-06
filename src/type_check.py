def check(AST):
    pass

def to_int(s):
    try:
        num = int(s)
        return num
    except ValueError:
        return
def to_float(s):
    try:
        num = float(s)
        return num
    except ValueError:
        return

def get_type(v):
    if v == "false" or v == "true":
        return "bool"
    elif to_int(v):
        return "int"
    elif to_float(v):
        return "float"
    return "str"

def is_numeric(t):
    return t in ["int", "float"]

def result_type(t1, t2):
    if "float" in [t1, t2]:
        return "float"
    return "int"

def check_op(x, op, y):
    t1 = get_type(x)
    t2 = get_type(y)
    print(f"\nt1: {t1} and t2: {t2}") # debug
    
    # Rule 1: No implicit type coercion is allowed.
        # Both operands must have the same type 
    if t1 == "str" and t2 != "str" or t1 != "str" and t2 == "str":
        return f"TypeError: {t1} '{op}' {t2} not allowed"

# Rule 2: Define which operators are valid for each type.
    # Addition:
    # - allowed for numeric types (int, float)
    # - allowed for strings (concatenation)
    if op == "+":
        if is_numeric(t1) and is_numeric(t2):
            return f"OK -> {result_type(t1, t2)}"
        if t1 == "str":
            return "OK -> '+' string"
        return f"TypeError: '+' not allowed for {t1}"

    # Arithmetic operators:
    if op in ["-", "*", "/"]:
        if is_numeric(t1) and is_numeric(t2):
            return f"OK -> {result_type(t1, t2)}"
        return f"TypeError: '{op}' not allowed for {t1}"
    # Comparison operators:
    if op in ["<", ">", "<=", ">=", "==", "!="]:
        if is_numeric(t1) and is_numeric(t2):
            return f"OK -> bool"
        return f"TypeError: '{op}' not allowed for {t1}"
    # Logical operators:
    if op in ["and", "or", "not"]:
        if t1 == "bool" and t2 == "bool":
            return f"OK -> bool"
        return f"TypeError: '{op}' not allowed for {t1}"

    return "Unknown operator"
    #sortering af typecheckeren (bools, ints, floats that can be added to ints)

    #dynamic, so you should be able to change types during runtime (find out if its typechecker or just parser)
    #how to do the shit on the line aboce

# Diff. tests
print(check_op("8", "+", "2"))
print(check_op("8", "-", "2"))
print(check_op("8", "*", "2.1"))
print(check_op("2.1", "*", "3"))
print(check_op("hello", "+", " world"))
print(check_op("hello", "+", "2"))
print(check_op("false", "+", "Hello"))
print(check_op("9", "+", "Hello"))
print(check_op("8", "*", "2"))
print(check_op("8", "*", "true"))
print(check_op("false", "*", "true"))
print(check_op("8", "*", "2"))
print(check_op("8", "*", "true"))
print(check_op("false", "*", "true"))
print(check_op("8", "<", "2"))
print(check_op("true", "or", "false"))
print(check_op("true", "and", "false"))
print(check_op("true", "not", "false"))
