from lark import Lark
from lark.indenter import Indenter

# GRAMMAR
grammar = r"""
start: stmt+
?stmt: create_stmt
| create_struct
| assign_stmt
| if_stmt
| while_stmt
| dowhile_stmt
| forrange_stmt
| foreach_stmt
| func_def
| return_stmt
| expr_stmt

// STATEMENTS
create_stmt: "create" NAME ("is" expr)? NEWLINE

create_struct: "create" NAME ("from" NAME)* "with:" NEWLINE INDENT (NAME ("is" expr)? NEWLINE)* DEDENT

assign_stmt: NAME ("from" NAME)* "is" expr NEWLINE

if_stmt: "if" cond "do:" NEWLINE INDENT stmt+ DEDENT ("else" "if" cond "do:" NEWLINE INDENT stmt+ DEDENT)* ("else" "do:" NEWLINE INDENT stmt+ DEDENT)?

while_stmt: "while" cond "do:" NEWLINE INDENT stmt+ DEDENT

dowhile_stmt: "do:" NEWLINE INDENT stmt* DEDENT "while" cond NEWLINE

forrange_stmt: "for each" NAME "between" expr "and" expr "do:" NEWLINE INDENT stmt* DEDENT

foreach_stmt: "for each" NAME "in" NAME "do:" NEWLINE INDENT stmt* DEDENT

func_def: "define" NAME params ":" NEWLINE INDENT stmt* DEDENT
params: "with" NAME ("," NAME)*

return_stmt: "return" expr NEWLINE

expr_stmt: expr NEWLINE

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
?expr: expr2 | "between " expr2 " and " expr2 | "chance " expr2 "%" | "chance " expr2 " in " expr2 | "chance " expr2
?expr2: expr3 | expr2 "+" expr3 | expr2 "-" expr3
?expr3: expr4 | expr3 "*" expr4 | expr3 "/" expr4
?expr4: expr5 | expr5 "^" expr4
?expr5: "-" expr5 | "(" expr ")" | INTEGER | FLOAT | STRING | NAME ("from" NAME)* | call_expr

// TOKENS
NAME: /[A-Z][a-zA-Z0-9_]*/
FLOAT: /([1-9][0-9]*|0)\.[0-9]+/
INTEGER: /[0-9]+/
STRING: /"[^"]*"/
call_expr: "call" NAME args?
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
