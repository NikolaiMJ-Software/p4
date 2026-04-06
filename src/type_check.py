x = 8
y = True
if isinstance(x, int) and isinstance(y, int):
    print("yes, int")
elif isinstance(x, str) and isinstance(y, str):
    print("yes, string")
elif isinstance(x, bool) and isinstance(y, bool):
    print("yes, bool")
elif isinstance(x, float) and isinstance(y, float):
    print("yes, float")
else:
    print("F, No")