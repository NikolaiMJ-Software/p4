from lark import Lark
from lark import Transformer, v_args
from lark.indenter import Indenter
from lark import Discard

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

struct_fields: struct_field*
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

# AST BUILDER
@v_args(inline=True)
class ASTBuilder(Transformer):
    
    # START
    def start(self, *statements):
        return list(statements)
    
    # STATEMENTS
    # creates
    def create_v(self, *items):
        return Create_v(items)
    def create_s(self, *items):
        return Create_s(items)
    def create_l(self, *items):
        return Create_l(items)

    # tails
    def create_tail(self, value):
        return value
    def struct_tail(self, *items):
        return items
    def list_tail(self, value):
        return value

    # struct specifics
    def struct_inheritance(self, item):
        return item
    def struct_fields(self, *items):
        return list(items)
    def struct_field(self, *items):
        return Create_v(items)

    # list specifics
    def list_items(self, *values):
        return list(values) # no ListItems class needed

    # general statements
    def assign_stmt(self, *values):
        return Assign(values)
    def if_stmt(self, *items):
        return If(items)
    def while_stmt(self, *items):
        return While(items)
    def dowhile_stmt(self, *items):
        return Dowhile(items)
    def forrange_stmt(self, *items):
        return Forrange(items)
    def foreach_stmt(self, *items):
        return Foreach(items)
    def func_def(self, *items):
        return Define(items)
    def return_stmt(self, value):
        return Return(value)
    def expr_stmt(self, value):
        return Expression(value)
    def input_stmt(self, value):
        return Input(value)
    def output_stmt(self, value):
        return Output(value)

    # EXPRESSIONS
    def or_expr(self, *values):
        return OrExpr(values) 
    def and_expr(self, *values):
        return AndExpr(values) 
    def not_expr(self, value):
        return NotExpr(value) 
    def equal_expr(self, *values):
        return EqualExpr(values)
    def not_equal_expr(self, *values):
        return NotEqualExpr(values)
    def greater_expr(self, *values):
        return GreaterExpr(values)
    def less_expr(self, *values):
        return LessExpr(values)
    def greater_equal_expr(self, *values):
        return GreaterEqualExpr(values)
    def less_equal_expr(self, *values):
        return LessEqualExpr(values)
    def between(self, left, right):
        return Between(left, right)
    def chance_percent(self, value):
        return Chance(value, 100)
    def chance(self, left, right):
        return Chance(left, right)
    def add(self, left, right):
        return Add(left, right)
    def sub(self, left, right):
        return Add(left, Neg(right))
    def mul(self, left, right):
        return Mul(left, right)
    def div(self, left, right):
        return Div(left, right)
    def pow(self, left, right):
        return Pow(left, right)
    def neg(self, value):
        return Neg(value)

    # TOKENS
    def ID(self, token):
        return str(token)
    def INTEGER(self, token):
        return int(token)
    def FLOAT(self, token):
        return float(token)
    def STRING(self, token):
        return str(token)[1:-1]  # Remove quotes
    def BOOL(self, token):
        if token in ("true", "1"):
            return True
        else:
            return False
    def call_expr(self, *items):
        return Call(items)
    def args(self, *items):
        return list(items)
    def params(self, *items):
        return list(items)
    def list_item(self, value):
        return value
    def NEWLINE(self, token):
        return Discard
    def INDENT(self, token):
        return Discard
    def DEDENT(self, token):
        return Discard
    
# CLASSES FOR AST

## BoolOp classes
class OrExpr:
    def __init__(self, values):
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"Or({self.cond},{self.cond2})"
class AndExpr:
    def __init__(self, values):
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"And({self.cond},{self.cond2})"
class NotExpr:
    def __init__(self, value):
        self.cond = value
    def __repr__(self):
        return f"Not({self.cond})"
class EqualExpr:
    def __init__(self, values):
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"Equal({self.cond},{self.cond2})"
class NotEqualExpr:
    def __init__(self, values):
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"NotEqual({self.cond},{self.cond2})"
class GreaterExpr:
    def __init__(self, values):
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"Greater({self.cond},{self.cond2})"
class LessExpr:
    def __init__(self, values):
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"Less({self.cond},{self.cond2})"
class GreaterEqualExpr:
    def __init__(self, values):
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"GreaterEqual({self.cond},{self.cond2})"
class LessEqualExpr:
    def __init__(self, values):
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"LessEqual({self.cond},{self.cond2})"

# STATEMENTS

# creates
class Create_v: # variable creation
    def __init__(self, values):
        self.name = values[0]
        self.value = None
        if len(values) > 1:
            self.values = values[1]
    def __repr__(self):
        return f"Create_v({self.name},{self.value})"
        
class Create_s: # struct creation
    def __init__(self, values):
        self.name = values[0]
        self.base = None
        self.fields = []
        if isinstance(values[1][0], list):
            self.base = None
            self.fields = values[1]
        else:
            self.base = values[1][0]
            self.fields = values[1][1]
    def __repr__(self):
        return f"Create_s({self.name},{self.base},{self.fields})"

class Create_l: # list creation
    def __init__(self, values): # receives name + list (values)
        self.name = values[0] # first (values[0]) is always name
        self.listing = values[1] # 1: means from 1 and onwards
    def __repr__(self):
        return f"Create_l({self.name},{self.listing})"
    
class Define:
    def __init__(self, values):
        self.name = values[0]
        if isinstance(values[1], list):
            self.params = values[1]
            self.body = list(values[2:])
        else:
            self.params = []
            self.body = list(values[1:])
    def __repr__(self):
        return f"Define({self.name},{self.params},{self.body})"
class If:
    def __init__(self, values):
        self.cond = values[0]
        self.body = list(values[1:])
    def __repr__(self):
        return f"If({self.cond},{self.body})"
class While:
    def __init__(self, values):
        self.cond = values[0]
        self.body = list(values[1:])
    def __repr__(self):
        return f"While({self.cond},{self.body})"
class Dowhile:
    def __init__(self, values):
        self.body = list(values[:-1])
        self.cond = values[-1]
    def __repr__(self):
        return f"Dowhile({self.body},{self.cond})"
class Forrange:
    def __init__(self, values):
        self.name = values[0]
        self.start = values[1]
        self.end = values[2]
        self.body = list(values[3:])
    def __repr__(self):
        return f"Forrange({self.name},{self.start},{self.end},{self.body})"
class Foreach:
    def __init__(self, values):
        self.name = values[0]
        self.collection = values[1]
        self.body = list(values[2:])
    def __repr__(self):
        return f"Foreach({self.name},{self.collection},{self.body})"
class Return:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Return({self.value})"
class Expression:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Expr({self.value})"
class Input:
    def __init__(self, value):
        self.name = value
    def __repr__(self):
        return f"Input({self.name})"
class Output:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Output({self.value})"
class Assign:
    def __init__(self, values):
        self.name = values[0]
        self.value = values[1]
    def __repr__(self):
        return f"Assign({self.name} is {self.value})"
class Between:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Between({self.left},{self.right})"
class Chance:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Chance({self.left},{self.right})"
class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Add({self.left},{self.right})"
class Mul:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Mul({self.left},{self.right})"
class Div:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Div({self.left},{self.right})"
class Pow:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Pow({self.left},{self.right})"
class Neg:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Neg({self.value})"
class Call:
    def __init__(self, values):
        self.name = values[0]
        self.args = list(values[1:])
    def __repr__(self):
        return f"Call({self.name},{self.args})"
# TEST
code = """create X with:
    A is 5
    B is 10
create Z is 10
"""

def create_ast(code):
    tree = parser.parse(code)
    ast = ASTBuilder().transform(tree)
    return ast

ast = create_ast(code)
print(ast)