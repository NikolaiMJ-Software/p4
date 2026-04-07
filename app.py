from src import parser, type_check

# TEST
code = """define Fun with Var1, Var2:
    create X is (5*8)^(2-1)
    if Var1 less than Var2 do:
        if Var2 do:
            return Var2
        if Var1 do:
            return Var1
    return X
"""

if __name__ == '__main__':
    AST = parser.create_AST(code)
    type_check.check(AST)