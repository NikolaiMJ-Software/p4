from lark import Transformer, v_args
from lark import Discard


# CLASSES FOR AST
import re
class ASTNode:
    def accept(self, visitor):
        snake_case_string = re.sub(r"(?<!^)(?=[A-Z])", "_", type(self).__name__).lower()
        method_name = f"visit_{snake_case_string}"
        visitor_method = getattr(visitor, method_name)
        return visitor_method(self)
# classes for litterals
class IntLiteral(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Int({self.value})"
class FloatLiteral(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Float({self.value})"
class StringLiteral(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"String({self.value})"
class BoolLiteral(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Bool({self.value})"

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
        return IntLiteral(int(token))

    def FLOAT(self, token):
        return FloatLiteral(float(token))

    def STRING(self, token):
        return StringLiteral(str(token)[1:-1])

    def BOOL(self, token):
        return BoolLiteral(token in ("true", "1"))
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
    

## BoolOp classes
class OrExpr(ASTNode):
    def __init__(self, values):
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"Or({self.cond},{self.cond2})"
class AndExpr(ASTNode):
    def __init__(self, values):
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"And({self.cond},{self.cond2})"
class NotExpr(ASTNode):
    def __init__(self, value):
        self.cond = value
    def __repr__(self):
        return f"Not({self.cond})"
class EqualExpr(ASTNode):
    def __init__(self, values):
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"Equal({self.cond},{self.cond2})"
class NotEqualExpr(ASTNode):
    def __init__(self, values):
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"NotEqual({self.cond},{self.cond2})"
class GreaterExpr(ASTNode):
    def __init__(self, values):
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"Greater({self.cond},{self.cond2})"
class LessExpr(ASTNode):
    def __init__(self, values):
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"Less({self.cond},{self.cond2})"
class GreaterEqualExpr(ASTNode):
    def __init__(self, values):
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"GreaterEqual({self.cond},{self.cond2})"
class LessEqualExpr(ASTNode):
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
class Add(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Add({self.left},{self.right})"
class Mul(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Mul({self.left},{self.right})"
class Div(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Div({self.left},{self.right})"
class Pow(ASTNode):
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