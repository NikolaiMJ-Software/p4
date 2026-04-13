from lark import Transformer, v_args
from lark import Discard

from src.ast.nodes import *

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
        name = items[0]
        if isinstance(items[1], list):
            params = items[1]
            body = list(items[2:])
        else:
            params = []
            body = list(items[1:])
        return Define(name, params, body)
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