from src.parser import parser
from src.ast import builder
from src.visitors import type_checker

# Help funtion to exictue integration test for type checker
def typecheck_test(code):
    tree = parser.parse(code)
    ast = builder.ASTBuilder().transform(tree)
    checker = type_checker.TypeCheckerVisitor()
    res = []
    for node in ast:
        res.append(checker.visit(node))
    # Return an array of the code's node types
    return res