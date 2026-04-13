from lark import Lark
from lark.indenter import Indenter

# GRAMMAR
grammar = r"""
start: stmt*
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
    | NEWLINE

// STATEMENTS
create_stmt: "create" ID create_tail? NEWLINE -> create_v
| "create" ID struct_tail -> create_s
| "create" ID list_tail NEWLINE -> create_l

create_tail: "is" expr
list_tail: "listing" list_items?
list_items: (list_item ",")* list_item
list_item: INTEGER | FLOAT | STRING | ID

struct_tail: struct_inheritance? "with:" NEWLINE INDENT struct_fields DEDENT

struct_inheritance: "from" ID

struct_fields: (struct_field | NEWLINE)*
struct_field: ID ("is" expr)? NEWLINE

assign_stmt: ID ("from" ID)? "is" expr NEWLINE

if_stmt: "if" expr "do:" NEWLINE INDENT stmt+ DEDENT ("else if" expr "do:" NEWLINE INDENT stmt+ DEDENT)* ("else do:" NEWLINE INDENT stmt+ DEDENT)?

while_stmt: "while" expr "do:" NEWLINE INDENT stmt+ DEDENT

dowhile_stmt: "do:" NEWLINE INDENT stmt* DEDENT "while" expr NEWLINE

forrange_stmt: "for each" ID "between" expr "and" expr "do:" NEWLINE INDENT stmt* DEDENT

foreach_stmt: "for each" ID "in" ID "do:" NEWLINE INDENT stmt* DEDENT

func_def: "define" ID params? ":" NEWLINE INDENT stmt* DEDENT
params: "with" ID ("," ID)*

return_stmt: "return" expr NEWLINE

expr_stmt: expr NEWLINE

input_stmt: "input in" ID NEWLINE

output_stmt: "output" expr NEWLINE

// EXPRESSIONS
?expr: expr2
    | expr "or" expr2 -> or_expr
?expr2: expr3
    | expr2 "and" expr3 -> and_expr
?expr3: expr4
    | "not" expr4 -> not_expr
?expr4: expr5
    | expr5 "equal" expr5 -> equal_expr
    | expr5 "not equal" expr5 -> not_equal_expr
    | expr5 "greater than" expr5 -> greater_expr
    | expr5 "less than" expr5 -> less_expr
    | expr5 "greater than or equal" expr5 -> greater_equal_expr
    | expr5 "less than or equal" expr5 -> less_equal_expr
?expr5: expr6
    | expr5 "+" expr6 -> add
    | expr5 "-" expr6 -> sub
?expr6: expr7
    | expr6 "*" expr7 -> mul
    | expr6 "/" expr7 -> div
?expr7: expr8
    | expr8 "^" expr7 -> pow
?expr8: "-" expr8 -> neg
    | "between" expr "and" expr -> between
    | "chance" expr "%" -> chance_percent
    | "chance" expr "in" expr -> chance
    | "(" expr ")"
    | INTEGER
    | FLOAT
    | STRING
    | BOOL
    | ID ("from" ID)?
    | call_expr

// TOKENS
ID: /[A-Z][a-zA-Z0-9_]*/
FLOAT: /([1-9][0-9]*|0)\.[0-9]+/
INTEGER: /[0-9]+/
STRING: /"[^"]*"/
BOOL: "true"|"false"|"1"|"0"
call_expr: "call" ID args?
args: "with" expr ("," expr)*

// IMPORTS & IGNORE
NEWLINE: (/\r?\n[ \t]*/)
%import common.WS_INLINE
%declare INDENT DEDENT
%ignore WS_INLINE

// Comments
COMMENT: /\#[^\n]*/
BLOCK_COMMENT: /\/\#[\s\S]*?\#\//
%ignore COMMENT
%ignore BLOCK_COMMENT
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

code = """create X with:
    A is 5
    B is 10
create Z is 10
"""

def parse(code):
    return parser.parse(code)