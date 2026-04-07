def check(AST):
    pass

# Get the type of a value
def get_type(v):
    # Bool
    if v in ["false", "true"]:
        return bool
    
    # Int
    try:
        int(v)
        return int
    except:
        pass
    
    # Float
    try:
        float(v)
        return float
    except:
        pass
    
    # Else string
    return str

# Check if 't' is a in or float
def is_numeric(t):
    return t in [int, float]

def check_op(val1, op, val2):
    # Get the type of the values
    t1 = get_type(val1)
    t2 = get_type(val2)
    
    # Connect only string with a string
    invalid_str = (t1 == str) != (t2 == str)
    
    # Addition works only on numbers and strings
    invalid_plus = op == "+" and not (is_numeric(t1) or t1 == str)
    
    # Arithmetic and comparison operators requre a number
    invalid_arith = op in ["-", "*", "/", "<", ">", "<=", ">=", "==", "!="] and not is_numeric(t1) and not is_numeric(t2)
    
    # Logical operators requre two bool types
    invalid_logic = op in ["and", "or", "not"] and t1 != bool
    
    # 'to' in for loops requres ints
    invalid_for_loop = op == "to" and t1 != int
    
    if invalid_str or invalid_plus or invalid_arith or invalid_logic or invalid_for_loop:
        return f"TypeError: unsupported operand type(s) for {op}: '{t1.__name__}' and '{t2.__name__}'"
    
    return f"OK -> {t1.__name__} {op} {t2.__name__}"
