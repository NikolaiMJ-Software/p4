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

def check_op(x, op, y):
    t1 = get_type(x)
    t2 = get_type(y)
    print(f"\nt1: {t1} vs t2: {t2}")
    is_t1_str = t1 == "str"
    is_t2_str = t2 == "str"
    
    # Rule 1: No implicit type coercion is allowed.
        # Both operands must have the same type 
    if is_t1_str and is_t2_str:
        print("str, only allowed '+'")
    elif is_t1_str and not is_t2_str:
        return f"TypeError: {type(t1)}{t1} {op} {type(t2)}{t2} not allowed"

# Rule 2: Define which operators are valid for each type.
    # Addition:
    # - allowed for numeric types (int, float)
    # - allowed for strings (concatenation)
    '''if op == "+":
        if t1 in ["int", "float", "string"]:
            return f"OK -> {t1}. The result is: {x+y}"
        return f"TypeError: + not allowed for {t1}"

    # Arithmetic operators:
    if op in ["-", "*", "/"]: #rember to add < and >
        if t1 in ["int", "float", "bool"]:
            return f"OK -> {t1}. The result is: {x*2 if op=='*' else x/y if op=='/' else x-y}"
        return f"TypeError: {op} not allowed for {t1}"

    # Comparison operators:
    if op in ["<", ">", "<=", ">="]:
        if t1 in ["int", "float"]:
            return f"OK -> {t1}. The result is: {x<y if op=='<' else x>y if op=='>' else x<=y if op=='<=' else x>=y}"
        return f"TypeError: {op} not allowed for {t1}"

    return "Unknown operator"
    #sortering af typecheckeren (bools, ints, floats that can be added to ints)

    #dynamic, so you should be able to change types during runtime (find out if its typechecker or just parser)
    #how to do the shit on the line aboce'''

#print(z)
print(check_op("8", "+", "2"))
print(check_op("8", "-", "2"))
print(check_op("8", "*", "2.1"))
print(check_op("2.1", "*", "3"))
print(check_op("hello", "+", " world"))
print(check_op("hello", "+", 2))
print(check_op("8", "*", "2"))
print(check_op("8", "*", "true"))
print(check_op("false", "*", "true"))