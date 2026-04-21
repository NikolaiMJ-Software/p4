import sys
from src.ast import builder
from src.parser import parser
from src.visitors import type_checker, interpreter



def load_source(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app.py <sourcefile>")
        sys.exit(1)

    source_path = sys.argv[1]
    code = load_source(source_path)

    tree = parser.parse(code)
    ast = builder.ASTBuilder().transform(tree)

    interp = interpreter.InterpreterVisitor()
    interp.run(ast)




"""
#TEST



def print_ast(node, indent=0):
    prefix = "  " * indent
    print(prefix + str(node))

    # ---- IF NODE ----
    if type(node).__name__ == "If":
        print(prefix + "  IF BODY:")
        for stmt in node.body:
            print_ast(stmt, indent + 2)

        if node.elifs:
            for cond, body in node.elifs:
                print(prefix + f"  ELIF ({cond}):")
                for stmt in body:
                    print_ast(stmt, indent + 2)

        if node.elses:
            print(prefix + "  ELSE:")
            for stmt in node.elses:
                print_ast(stmt, indent + 2)

    # ---- WHILE NODE ----
    elif type(node).__name__ == "While":
        print(prefix + "  WHILE BODY:")
        for stmt in node.body:
            print_ast(stmt, indent + 2)

    # ---- GENERIC BODY (functions etc.) ----
    elif hasattr(node, "body") and node.body:
        for child in node.body:
            print_ast(child, indent + 1)

if __name__ == '__main__':
    tree = parser.parse(code)
    ast = builder.ASTBuilder().transform(tree)

    print("---------AST--------\n")
    for stmt in ast:
        print_ast(stmt)
    
    print("\n---------TYPE CHECK--------\n")
    
    interpreter = interpreter.InterpreterVisitor(slot = 2)
    interpreter.run(ast)
    '''
    for node in ast:
        interpreter.visit(node)
    '''
    
    # TO DO:
    '''
    code = load_source() -> read a txt file

    tree = parser.parse(code)
    ast = ASTBuilder().transform(tree)

    TypeCheckerVisitor().visit(ast)

    InterpreterVisitor().visit(ast)
    '''
    '''
    checker = type_checker.TypeCheckerVisitor()
    for node in ast:
        checker.visit(node)
'''
"""