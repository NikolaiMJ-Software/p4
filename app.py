from src.ast import builder
from src.parser import parser
from src.visitors import type_checker

# TEST
code = """create HEJ with:
    Health is 2
    Defense
    Shield
create HEJ2 from HEJ with:
    Mom is 2
create HEJ3 from HEJ2 with:
    Dad is "hej"
    Mom is "med"
create X is Health from HEJ3
Defense from HEJ is "haj"
create Y is Defense from HEJ + Dad from HEJ3
create HEJ3 with:
    Dad is "hej"
    Mom is "med"
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
    
    checker = type_checker.TypeCheckerVisitor()
    for node in ast:
        checker.visit(node)
    
    # TO DO:
    '''
    code = load_source() -> read a txt file

    tree = parser.parse(code)
    ast = ASTBuilder().transform(tree)

    TypeCheckerVisitor().visit(ast)

    InterpreterVisitor().visit(ast)
    '''