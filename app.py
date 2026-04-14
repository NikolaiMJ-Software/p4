from src.ast import builder
from src.parser import parser
from src.visitors import type_checker

# TEST
code = """define Fun1 with Var1, Var2, Var3:
    create Y is Var1 * Var3
    create X is Y + Var2
    return X
call Fun1 with 1.2, 2, 2.2
"""


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
    print("---------AST--------\n")
    
    #checker = type_checker.TypeCheckerVisitor()
    #for node in ast:
        #checker.visit(node)
    
    # TO DO:
    '''
    code = load_source() -> read a txt file

    tree = parser.parse(code)
    ast = ASTBuilder().transform(tree)

    TypeCheckerVisitor().visit(ast)

    InterpreterVisitor().visit(ast)
    '''