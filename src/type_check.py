def check(AST):
    pass

x = 8
y = 2
z = x+y
def is_numeric_value(v):
    if isinstance(v, bool):
        return True
    if isinstance(v, (int, float)):
        return True
    if isinstance(v, str):
        try:
            int(v)    # should we perhaps do float(v)?
            return True
        except ValueError:
            return False
    return False

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