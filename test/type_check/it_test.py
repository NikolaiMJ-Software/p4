from src.parser import parser
from src.ast import builder
from src.visitors import type_checker

# Help funtion to exictue integration test for type checker
def typecheck_test(code):
    tree = parser.parse(code)
    ast = builder.ASTBuilder().transform(tree)
    checker = type_checker.TypeCheckerVisitor()
    last_return = []
    for node in ast:
        last_return.append(checker.visit(node))
    return last_return