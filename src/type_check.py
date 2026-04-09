from src.parser import Add, Mul, Define, Create, Div

def check(node, indent=0):
    print("  " * indent, node)
    body = getattr(node, "body", None)
    if body:
        for child in body:
            check(child, indent + 1)
    elif getattr(node, "value", None):
        val = getattr(node, "value", None)
        valid_type = isinstance(val, int) or isinstance(val, float) or isinstance(val, str) or isinstance(val, bool)
        if not valid_type:
            check(val, indent +1 )
        #print(f"-------------> {node.value}", valid_type)
    else:
        valid_type = isinstance(node, int) or isinstance(node, float) or isinstance(node, str) or isinstance(node, bool)
        if valid_type:
            return node
        else:
            #print("VALUES: ", node.left, node.right)
            
            handler = handlers.get(type(node))
            if handler:
                print(handler(node))
            else:
                check(node.left)
                check(node.right)
            
            '''if node.left and not inspect.isclass(node.left):
                check(node.left, indent + 1)
            if node.right and not inspect.isclass(node.right):
                check(node.right, indent + 1)'''
                

def check_add(node):
    return check_op(node.left, "+", node.right)
def check_min(node):
    return check_op(node.left, "-", node.right)
def check_mul(node):
    return check_op(node.left, "*", node.right)
def check_div(node):
    return check_op(node.left, "/", node.right)
handlers = {
    Add: check_add,
    Mul: check_mul,
    Div: check_div,
}

# Check if 't' is a in or float
def is_numeric(t):
    return t in [int, float]

def check_op(val1, op, val2):
    # Get the type of the values
    t1 = type(val1)
    t2 = type(val2)
    
    # Connect only string with a string
    invalid_str = (t1 == str) != (t2 == str)
    
    # Addition works only on numbers and strings
    invalid_plus = op == "+" and not (is_numeric(t1) and is_numeric(t2) or t1 == str)
    
    # Arithmetic and comparison operators requre a number
    invalid_arith = op in ["-", "*", "/", "<", ">", "<=", ">=", "==", "!="] and not is_numeric(t1)
    
    # Logical operators requre two bool types
    invalid_logic = op in ["and", "or", "not"] and t1 != bool
    
    # 'to' in for loops requres ints
    invalid_for_loop = op == "to" and ((t1 == int) != (t2 == int)) 
    
    if invalid_str or invalid_plus or invalid_arith or invalid_logic or invalid_for_loop:
        return f"TypeError: unsupported operand type(s) for {op}: '{t1.__name__}' and '{t2.__name__}'"
    
    return f"OK -> {t1.__name__} {op} {t2.__name__}"