from src.ast import builder
from src.parser import parser
from src.visitors import type_checker, interpreter

# TEST
code = """
define X with A,B:
    output "Eurika!"
    create Y is A+B
    return Y
output call X with 1,2
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
    
    #for stmt in ast:
        #print_ast(stmt)
    #print("---------AST--------\n")
    
    #checker = type_checker.TypeCheckerVisitor()
    #for node in ast:
        #checker.visit(node)
    
    interpreter = interpreter.InterpreterVisitor()
    for node in ast:
        interpreter.visit(node)
    
    # TO DO:
    '''
    code = load_source() -> read a txt file

    tree = parser.parse(code)
    ast = ASTBuilder().transform(tree)

    TypeCheckerVisitor().visit(ast)

    InterpreterVisitor().visit(ast)
    '''