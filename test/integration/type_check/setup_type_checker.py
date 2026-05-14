from src.parser import parser
from src.ast import builder
from src.visitors.interpreter import InterpreterVisitor, RuntimeValue

def type_check_test(code):
    tree = parser.parse(code)
    ast = builder.ASTBuilder().transform(tree)

    runner = InterpreterVisitor(code, slot=999)
    res = []

    for node in ast:
        value = runner.visit(node)

        if isinstance(value, RuntimeValue):
            res.append(value.type)
        else:
            res.append(None)

    return res