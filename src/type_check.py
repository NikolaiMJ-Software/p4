def check(AST):
    pass

x = 8
y = "2"
#z = x+y


def get_type(v):
    if isinstance(v, bool):
        return "bool"
    elif isinstance(v, float):
        return "float"
    elif isinstance(v, int):
        return "int"
    elif isinstance(v, str):
        return "string"
    return "unknown"

def is_numeric(t):
    return t in ["int", "float"]

def result_type(t1, t2):
    if "float" in [t1, t2]:
        return "float"
    return "int"

def check_op(x, op, y):
    t1 = get_type(x)
    t2 = get_type(y)

# Rule 1: No implicit type coercion is allowed.
    # Both operands must have the same type 
    if t1 != t2 and not (is_numeric(t1) and is_numeric(t2)):
        return f"TypeError: {t1} {op} {t2} not allowed"

# Rule 2: Define which operators are valid for each type.
    # Addition:
    # - allowed for numeric types (int, float)
    # - allowed for strings (concatenation)
    if op == "+":
        if is_numeric(t1) and is_numeric(t2):
            return f"OK -> {result_type(t1, t2)}. The result is: {x+y}"
        elif t1 == "string":
            return f"OK -> string. The result is: {x+y}"
        return f"TypeError: + not allowed for {t1}"

    # Arithmetic operators:
    if op in ["-", "*", "/"]:
        if is_numeric(t1) and is_numeric(t2):
            return f"OK -> {result_type(t1, t2)}. The result is: {x-y if op=='-' else x*y if op=='*' else x/y}"
        return f"TypeError: {op} not allowed for {t1}"
    # Comparison operators:
    if op in ["<", ">", "<=", ">=", "==", "!="]:
        if is_numeric(t1) and is_numeric(t2):
            return f"OK -> bool. The result is: {x<y if op=='<' else x>y if op=='>' else x<=y if op=='<=' else x>=y}"
        return f"TypeError: {op} not allowed for {t1}"
    # Logical operators:
    if op in ["and", "or", "not"]:
        if t1 == "bool" and t2 == "bool":
            return f"OK -> bool. The result is: {x and y if op=='AND' else x or y}"
        return f"TypeError: {op} not allowed for {t1}"

    return "Unknown operator"
    #sortering af typecheckeren (bools, ints, floats that can be added to ints)

    #dynamic, so you should be able to change types during runtime (find out if its typechecker or just parser)
    #how to do the shit on the line aboce

def to_int(s):
    try:
        num = int(s)
        return num
    except ValueError:
        return ""
def to_float(s):
    try:
        num = float(s)
        return num
    except ValueError:
        return ""
def to_bool(s):
    try:
        num = bool(s)
        return num
    except ValueError:
        return ""
str1 = to_int("1")
str2 = to_float("1")
str3 = to_bool("1")

print(str1, str2, str3)
#print(z)
print(check_op(8, "+", 2))
print(check_op(8, "-", "2"))
print(check_op(8, "*", 2.1))
print(check_op(2.1, "*", 3))
print(check_op("hello", "+", " world"))
print(check_op(8, "*", 2))
print(check_op(8, "*", True))
print(check_op(False, "*", True))
print(check_op(8, "<", 2))
print(check_op(True, "or", False))
print(check_op(True, "and", False))
print(check_op(True, "not", False))