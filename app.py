from src.ast import builder
from src.parser import parser
from src.visitors import type_checker, interpreter
from src.parser import parse, ParseError
from src.type_check import TypeCheckError

#TEST
code = """
create X is 0
define State:
    while true do:
        output X
        X is X + 1
        if X equal 1000 do:
            stop

call State

"""


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

# function for making a node (instead of passing raw line + column)
# TODO: THIS IS ESSENTIAL FOR ERROR HANDLING (COORDINATES) BUT PROBABLY ISN'T IN THE RIGHT SPOT
def make_node(self, tree):
    return MyNode(
        ...,
        line=tree.meta.line,
        column=tree.meta.column
    )

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
    
    #interpreter = interpreter.InterpreterVisitor()
    #for node in ast:
        # interpreter.visit(node)
        # checker.visit(node)

    try:
        tree = parse(code) # parse code, save as tree (not format, just name)
        ast = builder.ASTBuilder().transform(tree) # build ast from tree

        checker = type_checker.TypeCheckerVisitor(code) # needs code passing
        for node in ast:
            checker.visit(node)

        print("Success!")

    except ParseError as e:
        print(f"[Syntax Error] Line {e.line}, Column {e.column}")
        print(e.context)

    except TypeCheckError as e:
        print(f"[Type Error] {e}")
        if e.line:
            print(f"Line {e.line}, Column {e.column}")
        if e.context:
            print(e.context)
    
    except Exception as e:
        print("[Internal Error]", e)

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