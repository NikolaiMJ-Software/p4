# Check if 't' is a in or float
def is_numeric(t):
    return t in [int, float]

def get_type(val1, val2):
    if float in (val1, val2):
        return float
    elif int in (val1, val2):
        return int
    return val1

def check_op(val1, op, val2):
    # Get the type of the values
    t1 = val1 if isinstance(val1, type) else type(val1)
    t2 = val2 if isinstance(val2, type) else type(val2)
    
    # Connect only string with a string
    invalid_str = (t1 == str) != (t2 == str)
    
    # Addition works only on numbers and strings
    invalid_plus = op == "+" and not (is_numeric(t1) and is_numeric(t2) or t1 == str)
    
    # Arithmetic and comparison operators requre a number
    invalid_arith = op in ["-", "*", "/", "<", ">", "<=", ">=", "==", "!=", "^"] and not (is_numeric(t1) and is_numeric(t2))
    
    # Logical operators requre two bool types
    invalid_logic = op in ["and", "or", "not"] and t1 != bool
    
    # 'to' in for loops requres ints
    invalid_for_loop = op == "to" and ((t1 == int) != (t2 == int)) 
    # 'between' requires two numerics
    invalid_between = op == "between" and not (is_numeric(t1) and is_numeric(t2))   
    # 'chance' requires two numerics
    invalid_chance = op == "chance" and not (is_numeric(t1) and is_numeric(t2))    

    if invalid_str or invalid_plus or invalid_arith or invalid_logic or invalid_for_loop or invalid_between or invalid_chance:
        return f"TypeError: unsupported operand type(s) for {op}: '{t1.__name__}' and '{t2.__name__}'"
    
    print(f"OK -> {t1.__name__} {op} {t2.__name__}")
    return get_type(t1, t2)