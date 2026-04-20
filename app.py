from src.ast import builder
from src.parser import parser
from src.visitors import type_checker
from src.parser import parse, ParseError
from src.type_check import TypeCheckError

# TEST
code = """define Fun1 with Var1, Var2, Var3:
    create Y is Var1 * Var3
    create X is Y + Var2
    create Var2
    return Y
call Fun1 with 1.2, 2, 2.2
call Fun with 1, 2
"""


def print_ast(node, indent = 0):
    print("  " * indent, node)
    body = getattr(node, "body", None)
    if body:
        for child in body:
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
    # tree = parser.parse(code)
    # ast = builder.ASTBuilder().transform(tree)
    # for stmt in ast:
    #     print_ast(stmt)
    # print("---------AST--------\n")
    
    #checker = type_checker.TypeCheckerVisitor()
    #for node in ast:
        #checker.visit(node)

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