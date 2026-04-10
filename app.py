from src.ast import builder
from src.parser import parser
from src.visitors import type_checker

# TEST
code = """create X is 1 + 1
"""

''' --------- Second test --------
define Fun with Var1, Var2:
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
'''


def print_ast(node, indent = 0):
    print("  " * indent, node)
    body = getattr(node, "body", None)
    if body:
        for child in body:
            print_ast(child, indent + 1)

if __name__ == '__main__':
    tree = parser.parse(code)
    ast = builder.ASTBuilder().transform(tree)
    for stmt in ast:
        print_ast(stmt)
    
    checker = type_checker.TypeCheckerVisitor()
    checker.visit(ast[0])
    
    # TO DO:
    '''
    code = load_source() -> read a txt file

    tree = parser.parse(code)
    ast = ASTBuilder().transform(tree)

    TypeCheckerVisitor().visit(ast)

    InterpreterVisitor().visit(ast)
    '''