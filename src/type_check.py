def check(AST):
    pass

x = 8
y = "2"
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


if is_numeric_value(x) and is_numeric_value(y):
    print(z)
else:
    print("F, No")

if isinstance(x, int) and isinstance(y, int):
    print("yes, int")
elif isinstance(x, str) and isinstance(y, str):
    print("yes, string")
elif isinstance(x, bool) and isinstance(y, bool):
    print("yes, bool")
elif isinstance(x, float) and isinstance(y, float):
    print("yes, float")
else:
    print("Ff, No")

    #sortering af typecheckeren (bools, ints, floats that can be added to ints)

    #dynamic, so you should be able to change types during runtime (find out if its typechecker or just parser)
    #how to do the shit on the line aboce