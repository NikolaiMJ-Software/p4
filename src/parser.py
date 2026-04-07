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
create_stmt: "create" ID create_tail? NEWLINE | "create" ID struct_tail

create_tail: "is" expr

struct_tail: struct_inheritance? "with:" NEWLINE INDENT struct_fields DEDENT

struct_inheritance: "from" ID ("from" ID)*

struct_fields: struct_field*
struct_field: ID ("is" expr)? NEWLINE

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

// CONDITIONS -> change to boolean operators
?cond: cond2
    | cond "or" cond2 -> or_bool_op
?cond2: cond3
    | cond2 "and" cond3 -> and_bool_op
?cond3: cond4
    | "not" cond4 -> not_bool_op
?cond4: expr
    | expr "equal" expr -> equal_bool_op
    | expr "not equal" expr -> not_equal_bool_op
    | expr "greater than" expr -> greater_bool_op
    | expr "less than" expr -> less_bool_op
    | expr "greater than or equal" expr -> greater_equal_bool_op
    | expr "less than or equal" expr -> less_equal_bool_op


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
            return {
                "type": "create",
                "name": items[0],
                "value": None,
            }
        if len(items) == 2 and isinstance(items[1], dict) and items[1].get("type") == "struct_tail":
            return {
                "type": "create_struct",
                "name": items[0],
                "bases": items[1]["bases"],
                "fields": items[1]["fields"],
            }
        if len(items) == 2:
            return {
                "type": "create",
                "name": items[0],
                "value": items[1],
            }
        raise Exception("Invalid create statement")

    def create_tail(self, value):
        return value
    
    def struct_tail(self, *items):
        bases = []
        fields = []
        for item in items:
            if isinstance(item, dict) and item.get("type") == "struct_inheritance":
                bases = item["bases"]
            elif isinstance(item, list):
                fields = item
        return {
            "type": "struct_tail",
            "bases": bases,
            "fields": fields,
        }
    
    def struct_inheritance(self, *items):
        return {
            "type": "struct_inheritance",
            "bases": list(items),
        }
    
    def struct_fields(self, *items):
        return list(items)

    def struct_field(self, *items):
        if len(items) == 1:
            return {
                "name": items[0],
                "value": None,
            }
        return {
            "name": items[0],
            "value": items[1],
        }
    
    def assign_stmt(self, *values):
        return Assign(values) # previously: ("assign(" + ",".join(str(i) for i in items) + ")")
    
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
        return Define(items)
    
    def return_stmt(self, value):
        return Return(value)
    
    def expr_stmt(self, value):
        return Expression(value)
    
    def input_stmt(self, value):
        return Input(value)
    
    def output_stmt(self, value):
        return Output(value)
    
    # BOOLEAN OPERATORS
    def or_bool_op(self, values):
        return OrBoolOp(values) # ("or(" + str(left) + "," + str(right) + ")")
    
    def and_bool_op(self, values):
        return AndBoolOp(values) # ("and(" + str(left) + "," + str(right) + ")")
    
    def not_bool_op(self, value):
        return NotBoolOp(value) # ("not(" + str(value) + ")")
    
    def equal_bool_op(self, values):
        return EqualBoolOp(values) # ("equal(" + str(left) + "," + str(right) + ")")
    
    def not_equal_bool_op(self, values):
        return NotEqualBoolOp(values) # ("not_equal(" + str(left) + "," + str(right) + ")")

    def greater_bool_op(self, values):
        return GreaterBoolOp(values) # ("greater(" + str(left) + "," + str(right) + ")")
    
    def less_bool_op(self, values):
        return LessBoolOp(values) # ("less(" + str(left) + "," + str(right) + ")")
    
    def greater_equal_bool_op(self, values):
        return GreaterEqualBoolOp(values) # ("greater_equal(" + str(left) + "," + str(right) + ")")
    
    def less_equal_bool_op(self, values):
        return LessEqualBoolOp(values) # Less("less_equal(" + str(left) + "," + str(right) + ")")

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
        return ("neg(" + value + ")")

    # TOKENS
    def ID(self, token):
        return str(token)

    def INTEGER(self, token):
        return int(token)
    
    def FLOAT(self, token):
        return float(token)
    
    def STRING(self, token):
        return str(token)[1:-1]  # Remove quotes
    
    def call_expr(self, *items):
        return ("call(" + ",".join(str(i) for i in items) + ")")
    
    def args(self, *items):
        return list(items)
    
    def NEWLINE(self, token):
        return Discard
    
    def INDENT(self, token):
        return Discard
    
    def DEDENT(self, token):
        return Discard
    
# CLASSES FOR AST

## BoolOp classes
class OrBoolOp:
    def __init(self, values):
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"Or({this.cond} or {this.cond2})"
class AndBoolOp:
    def __init(self, values):
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"And({this.cond} and {this.cond2})"
class NotBoolOp:
    def __init(self, value):
        self.cond = value
    def __repr__(self):
        return f"Not({this.cond})"
class EqualBoolOp:
    def __init(self, values):
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"Equal({this.cond} equals {this.cond2})"
class NotEqualBoolOp:
    def __init(self, values):
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"NotEqual({this.cond} not equals {this.cond2})"
class GreaterBoolOp:
    def __init(self, values):
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"Greater({this.cond} greater than {this.cond2})"
class LessBoolOp:
    def __init(self, values):
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"Less({this.cond} less than {this.cond2})"
class GreaterEqualBoolOp:
    def __init(self, values):
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"GreaterEqual({this.cond} greater than or equals {this.cond2})"
class LessEqualBoolOp:
    def __init(self, values):
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"LessEqual({this.cond} less than or equals {this.cond2})"
class Define: ## NOT FULLY IMPLEMENTED YET
    def __init__(self, values):
        self.name = values[0]
    def __repr__(self):
        return f"Define({self.name},{self.params},{self.body})"
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
        # x is 5
        # TODO: maybe add multiple assigns in one line
        self.name = values[0]
        self.value = values[1]
        
        # self.name = name
        # self.value = value
    def __repr__(self):
        return f"Assign({self.name} is {self.value})"
# TEST
code = """X is True
Y is False
X or Y
"""

try:
    tree = parser.parse(code)
    ast = ASTBuilder().transform(tree)
    print("Tree:", tree.pretty())
    print("AST:", ast)
except Exception as e:
    print("Parse error:", e)
