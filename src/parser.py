from lark import Lark
from lark import Transformer, v_args
from lark.indenter import Indenter
from lark import Discard

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

func_def: "define" ID params? ":" NEWLINE INDENT stmt* DEDENT
params: "with" ID ("," ID)*

return_stmt: "return" expr NEWLINE

expr_stmt: expr NEWLINE

input_stmt: "input in" ID NEWLINE

output_stmt: "output" expr NEWLINE

// CONDITIONS
?cond: cond2
    | cond "or" cond2 -> or_
?cond2: cond3
    | cond2 "and" cond3 -> and_
?cond3: cond4
    | "not" cond4 -> not_
?cond4: expr
    | expr "equal" expr -> equal_
    | expr "not equal" expr -> not_equal
    | expr "greater than" expr -> greater_
    | expr "less than" expr -> less_
    | expr "greater than or equal" expr -> greater_equal_
    | expr "less than or equal" expr -> less_equal_


// EXPRESSIONS
?expr: expr2
    | expr "+" expr2 -> add
    | expr "-" expr2 -> sub
?expr2: expr3
    | expr2 "*" expr3 -> mul
    | expr2 "/" expr3 -> div
?expr3: expr4
    | expr4 "^" expr3 -> pow
?expr4: "-" expr4 -> neg
    | "between" expr "and" expr -> between
    | "chance" expr "%" -> chance_percent
    | "chance" expr "in" expr -> chance
    | "(" expr ")"
    | INTEGER
    | FLOAT
    | STRING
    | ID ("from" ID)*
    | call_expr

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

# AST BUILDER (NOT FULLY IMPLEMENTED YET)
@v_args(inline=True)
class ASTBuilder(Transformer):
    
    # START
    def start(self, *statements):
        return list(statements)
    
    # STATEMENTS
    def create_stmt(self, *items):
        if len(items) == 1:
            return ("create(" + str(items[0]) + ")")
        elif len(items) == 2:
            return ("create(" + str(items[0]) + "," + str(items[1]) + ")")
        else:
            raise Exception("Invalid create statement")
    
    def assign_stmt(self, *items):
        return ("assign(" + ",".join(str(i) for i in items) + ")")
    
    def if_stmt(self, *items):
        return ("if(" + ",".join(str(i) for i in items) + ")")
    
    def while_stmt(self, *items):
        return ("while(" + ",".join(str(i) for i in items) + ")")
    
    def dowhile_stmt(self, *items):
        return ("do_while(" + ",".join(str(i) for i in items) + ")")
    
    def forrange_stmt(self, *items):
        return ("forrange(" + ",".join(str(i) for i in items) + ")")
    
    def foreach_stmt(self, *items):
        return ("foreach(" + ",".join(str(i) for i in items) + ")")

    def func_def(self, *items):
        return ("define(" + ",".join(str(i) for i in items) + ")")
    
    def return_stmt(self, value):
        return ("return(" + str(value) + ")")
    
    def expr_stmt(self, value):
        return value
    
    def input_stmt(self, value):
        return ("input(" + str(value) + ")")
    
    def output_stmt(self, *items):
        return ("output(" + str(items[0]) + ")")
    
    # CONDITIONS
    def or_(self, left, right):
        return ("or(" + str(left) + "," + str(right) + ")")
    
    def and_(self, left, right):
        return ("and(" + str(left) + "," + str(right) + ")")
    
    def not_(self, value):
        return ("not(" + str(value) + ")")
    
    def equal_(self, left, right):
        return ("equal(" + str(left) + "," + str(right) + ")")
    
    def not_equal_(self, left, right):
        return ("not_equal(" + str(left) + "," + str(right) + ")")

    def greater_(self, left, right):
        return ("greater(" + str(left) + "," + str(right) + ")")
    
    def less_(self, left, right):
        return ("less(" + str(left) + "," + str(right) + ")")
    
    def greater_equal_(self, left, right):
        return ("greater_equal(" + str(left) + "," + str(right) + ")")
    
    def less_equal_(self, left, right):
        return ("less_equal(" + str(left) + "," + str(right) + ")")

    # EXPRESSIONS
    def between(self, left, right):
        return ("between(" + str(left) + "," + str(right) + ")")
    
    def chance_percent(self, value):
        return ("chance(" + str(value) + "," + "100)")
    
    def chance(self, left, right):
        return ("chance(" + str(left) + "," + str(right) + ")")
    
    def add(self, left, right):
        return ("add(" + str(left) + "," + str(right) + ")")
    
    def sub(self, left, right):
        return ("sub(" + str(left) + "," + str(right) + ")")
    
    def mul(self, left, right):
        return ("mul(" + str(left) + "," + str(right) + ")")
    
    def div(self, left, right):
        return ("div(" + str(left) + "," + str(right) + ")")
    
    def pow(self, left, right):
        return ("pow(" + str(left) + "," + str(right) + ")")
    
    def neg(self, value):
        return ("neg(" + str(value) + ")")

    # TOKENS
    def ID(self, token):
        return str(token)

    def INTEGER(self, token):
        return int(token)
    
    def FLOAT(self, token):
        return float(token)
    
    def STRING(self, token):
        return str(token)[1:-1]  # Remove quotes
    
    def NEWLINE(self, token):
        return Discard
    
    def INDENT(self, token):
        return Discard
    
    def DEDENT(self, token):
        return Discard
    
# TEST
code = """for each Item between 1 and 100 do:
    if Item greater than 10 do:
        output Item
"""

try:
    tree = parser.parse(code)
    ast = ASTBuilder().transform(tree)
    print("Tree:", tree.pretty())
    print("AST:", ast)
except Exception as e:
    print("Parse error:", e)
