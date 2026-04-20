from src.ast import builder
from src.parser import parser
from src.visitors import type_checker, interpreter
from src.parser import parse, ParseError
from src.type_check import TypeCheckError

#TEST
code = """define Fun1 with Var1, Var2, Var3:
    create Y is Var1 * Var3
    create X is Y + Var2
    return X
call Fun1 with 1.2, 2, 2.2
create A is false
create D is true
if A do:
    create B is 5
else if D do:
    create C is 10
else do:
    create E is 15
while A do:
    create F is 20
# DOWHILE
create G is true
do:
    create H is 25
while G

# LISTS
create L listing: 1, 2, 3
index 1 of L is 5
create M listing: "a", "b", "c"
create O listing:
create Arr listing: 1, 2, 3
for each N from 1 to 5 do:
    create X is N + 1
for each Elem in Arr do:
    create Y is Elem + 2
    
create HEJ with:
    Health is 2
    Defense
    Shield
create HEJ2 from HEJ with:
    Mom is 2
create HEJ3 from HEJ2 with:
    Dad is "hej"
    Mom is "med"
Defense from HEJ is "mom"
Shield from HEJ2 is 4.2
Shield from HEJ3 is "Dig"
create Y is Shield from HEJ3 + Mom from HEJ3
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
    checker = type_checker.TypeCheckerVisitor()
    for node in ast:
        checker.visit(node)