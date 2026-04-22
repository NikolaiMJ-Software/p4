import sys
import traceback
from src.ast import builder
from src.visitors import type_checker
from src.visitors import interpreter
from src.parser import parse, ParseError
from src.errors import Error, TypeError, RuntimeError 

# To run your code use the following command in terminal "python app.py <file>" an example on the file could be test.rogue

def load_source(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def print_ast(node, indent=0):
    prefix = "  " * indent
    print(prefix + str(node))

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

    elif type(node).__name__ == "While":
        print(prefix + "  WHILE BODY:")
        for stmt in node.body:
            print_ast(stmt, indent + 2)

    elif hasattr(node, "body") and node.body:
        for child in node.body:
            print_ast(child, indent + 1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app.py <sourcefile>")
        sys.exit(1)

    source_path = sys.argv[1]

    try:
        code = load_source(source_path)

        tree = parse(code)
        ast = builder.ASTBuilder().transform(tree)

        print("---------AST--------\n")
        for stmt in ast:
            print_ast(stmt)

        print("\n---------TYPE CHECK--------\n")
        checker = type_checker.TypeCheckerVisitor(code)
        for node in ast:
            checker.visit(node)

        print("\n---------INTERPRETATION--------\n")
        interp = interpreter.InterpreterVisitor(slot=2)
        interp.run(ast)

        print("Success!")

    except ParseError as e:
        print(f"[Syntax Error] {e}")
        print(f"Line {e.line}, Col {e.column}")
        print(e.context)

    except TypeError as e:
        print(f"[Type Error] {e}")
        print(f"Line {e.line}, Col {e.column}")
        print(e.context)

    except RuntimeError as e:
        print(f"[Runtime Error] {e}")
        print(f"Line {e.line}, Col {e.column}")
        print(e.context)

    except Error as e:
        print(f"[Error] {e}")
        print(f"Line {e.line}, Col {e.column}")
        print(e.context)

    except Exception as e:
        print("[Internal Error]", e)
        traceback.print_exc()