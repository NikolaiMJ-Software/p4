from lark import Lark
from lark import Transformer, v_args
from lark.indenter import Indenter

# GRAMMAR
grammar = r"""
start: stmt+
?stmt: create_stmt
| assign_stmt
| if_stmt
| while_stmt
| dowhile_stmt
| forrange_stmt
| foreach_stmt
| func_def
| return_stmt
| expr_stmt
| input_stmt
| output_stmt

// STATEMENTS
create_stmt: "create" ID create_tail? NEWLINE | "create" ID struct_tail

create_tail: "is" expr

struct_tail: struct_inheritance? "with:" NEWLINE INDENT struct_fields DEDENT

struct_inheritance: "from" ID ("from" ID)*

struct_fields: (ID ("is" expr)? NEWLINE)*

assign_stmt: ID ("from" ID)* "is" expr NEWLINE

if_stmt: "if" cond "do:" NEWLINE INDENT stmt+ DEDENT ("else if" cond "do:" NEWLINE INDENT stmt+ DEDENT)* ("else do:" NEWLINE INDENT stmt+ DEDENT)?

while_stmt: "while" cond "do:" NEWLINE INDENT stmt+ DEDENT

dowhile_stmt: "do:" NEWLINE INDENT stmt* DEDENT "while" cond NEWLINE

forrange_stmt: "for each" ID "between" expr "and" expr "do:" NEWLINE INDENT stmt* DEDENT

foreach_stmt: "for each" ID "in" ID "do:" NEWLINE INDENT stmt* DEDENT

func_def: "define" ID params ":" NEWLINE INDENT stmt* DEDENT
params: "with" ID ("," ID)*

return_stmt: "return" expr NEWLINE

expr_stmt: expr NEWLINE

input_stmt: "input in" ID NEWLINE

output_stmt: "output" expr NEWLINE

// CONDITIONS
?cond: cond2 | cond "or" cond2
?cond2: cond3 | cond2 "and" cond3
?cond3: cond4 | "not" cond4
?cond4: expr
    | expr "equal" expr
    | expr "not equal" expr
    | expr "greater than" expr
    | expr "less than" expr
    | expr "greater than or equal" expr
    | expr "less than or equal" expr


// EXPRESSIONS
?expr: expr2 | "between" expr2 "and" expr2 | "chance" expr2 "%" | "chance" expr2 "in" expr2 | "chance" expr2
?expr2: expr3 | expr2 "+" expr3 | expr2 "-" expr3
?expr3: expr4 | expr3 "*" expr4 | expr3 "/" expr4
?expr4: expr5 | expr5 "^" expr4
?expr5: "-" expr5 | "(" expr ")" | INTEGER | FLOAT | STRING | ID ("from" ID)* | call_expr

// TOKENS
ID: /[A-Z][a-zA-Z0-9_]*/
FLOAT: /([1-9][0-9]*|0)\.[0-9]+/
INTEGER: /[0-9]+/
STRING: /"[^"]*"/
call_expr: "call" ID args?
args: "with" expr ("," expr)*

// IMPORTS & IGNORE
NEWLINE: (/\r?\n[ \t]*/)
%import common.WS_INLINE
%declare INDENT DEDENT
%ignore WS_INLINE
"""

class TreeIndenter(Indenter):
    NL_type = 'NEWLINE'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = 'INDENT'
    DEDENT_type = 'DEDENT'
    tab_len = 8

# PARSER
parser = Lark(
    grammar,
    parser="lalr",
    start="start",
    postlex=TreeIndenter()
)

# AST BUILDER (NOT IMPLEMENTED YET)
@v_args(inline=True)
class ASTBuilder(Transformer):

    # --- TOKENS ---
    def ID(self, token):
        return str(token)

    def INTEGER(self, token):
        return int(token)
    
    # --- EXPRESSIONS ---
    def expr(self, value):
        return value

    # --- STATEMENTS ---
    def create_stmt(self, *items):
        print("create_stmt items:", items)
        return items

    # --- ROOT ---
    def start(self, *statements):
        return list(statements)
    
# TEST
code = """define Fun with Var1, Var2:
    create X is (5*8)^(2-1)
    if Var1 less than Var2 do:
        if Var2 do:
            return Var2
        if Var1 do:
            return Var1
    return X
"""

try:
    tree = parser.parse(code)
    print(tree.pretty())
except Exception as e:
    print("Parse error:", e)
