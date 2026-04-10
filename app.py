from src import parser, type_check

# TEST
code = """define Fun with Var1, Var2:
    create X is (5*8)^(2+1)
    create Y is 2+1
    create Z is "hej"
    Y is Y + Z
    if Var1 less than Var2 do:
        if Var2 do:
            return Var2
        if Var1 do:
            return Var1
    return X
"""

if __name__ == '__main__':
    AST = parser.create_ast(code)
    for stmt in AST:
        type_check.check(stmt)
    
    # TO DO:
    '''
    code = load_source() -> read a txt file

    tree = parser.parse(code)
    ast = ASTBuilder().transform(tree)

    TypeCheckerVisitor().visit(ast)

    InterpreterVisitor().visit(ast)
    '''