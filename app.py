from src.ast import builder
from src.parser import parser
from src.visitors import type_checker

#tes
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
create M listing: "a", "b", "c"
create O listing:
create Arr listing: 1, 2, 3
for each N from 1 to 5 do:
    create X is N + 1
for each Elem in Arr do:
    create Y is Elem + 2
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
    tree = parser.parse(code)
    ast = builder.ASTBuilder().transform(tree)

    print("---------AST--------\n")
    for stmt in ast:
        print_ast(stmt)
    
    print("\n---------TYPE CHECK--------\n")
    
    checker = type_checker.TypeCheckerVisitor()
    for node in ast:
        checker.visit(node)