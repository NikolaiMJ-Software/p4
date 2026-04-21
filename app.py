from src.ast import builder
# from src.parser import parser # not needed here, only used by parse() in parser.py
from src.visitors import type_checker
# from src.visitors import interpreter # this doesn't exist anywhere, so commented out to avoid ImportError
from src.parser import parse, ParseError
from src.errors import Error, TypeError, RuntimeError # , SyntaxError # replaced by ParseError

#TEST
code = """
create A is B
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

if __name__ == '__main__':
    try:
        tree = parse(code) # parse code, save as tree (not format, just name)
        ast = builder.ASTBuilder().transform(tree) # build ast from tree

        print("---------AST--------\n")
        for stmt in ast:
            print_ast(stmt)

        print("\n---------TYPE CHECK--------\n")
        checker = type_checker.TypeCheckerVisitor(code) # needs code passing
        for node in ast:
            checker.visit(node)

        print("Success!")

    except ParseError as e:
        print(f"[Syntax Error] Line {e.line}, Col {e.column}")
        print(e.context)
    
    except TypeError as e:
        print(f"[Type Error] Line {e.line}, Col {e.column}")
        print(e.context)
    
    except RuntimeError as e:
        print(f"[Runtime Error] Line {e.line}, Col {e.column}")
        print(e.context)

    except Error as e:
        print(f"[Error] {e}")  # fallback for any other Error subclass
    
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