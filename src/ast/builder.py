from lark import Transformer, v_args
from lark import Discard

from src.ast.nodes import *

# AST BUILDER
@v_args(inline=True, meta=True)
class ASTBuilder(Transformer):
    
    # START
    def start(self, meta, *statements):
        return list(statements)
    
    # STATEMENTS
    # creates
    def create_v(self, meta, *items):
        return Create_v(items)
    def create_s(self, meta, *items):
        return Create_s(items)
    def create_l(self, meta, *items):
        return Create_l(items)

    # tails
    def create_tail(self, meta, value):
        return value
    def struct_tail(self, meta, *items):
        return items
    def list_tail(self, meta, value):
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
    def assign_stmt(self, meta, *values):
        return Assign(values, meta.line, meta.column)
    def if_stmt(self, meta, *items):
        return If(items, meta.line, meta.column)
    def else_stmt(self, meta, *items):
        return list(items, meta.line, meta.column)
    def while_stmt(self, meta, *items):
        return While(items, meta.line, meta.column)
    def dowhile_stmt(self, meta, *items):
        return Dowhile(items, meta.line, meta.column)
    def forrange_stmt(self, meta, *items):
        return Forrange(items, meta.line, meta.column)
    def foreach_stmt(self, meta, *items):
        return Foreach(items, meta.line, meta.column)
    def func_def(self, meta, *items):
        name = items[0]
        if isinstance(items[1], list):
            params = items[1]
            body = list(items[2:])
        else:
            params = []
            body = list(items[1:])
        return Define(name, params, body, meta.line, meta.column)
    def return_stmt(self, meta, value):
        return Return(value, meta.line, meta.column)
    def expr_stmt(self, meta, value):
        return Expression(value)
    def input_stmt(self, meta, value):
        return Input(value, meta.line, meta.column)
    def output_stmt(self, meta, value):
        return Output(value, meta.line, meta.column)

    # EXPRESSIONS
    def or_expr(self, meta, *values):
        return OrExpr(values, meta.line, meta.column)
    def and_expr(self, meta, *values):
        return AndExpr(values, meta.line, meta.column)
    def either_expr(self, meta, *values):
        return XorExpr(values, meta.line, meta.column)
    def not_expr(self, meta, value):
        return NotExpr(value, meta.line, meta.column)
    def equal_expr(self, meta, *values):
        return EqualExpr(values, meta.line, meta.column)
    def not_equal_expr(self, meta, *values):
        return NotEqualExpr(values, meta.line, meta.column)
    def greater_expr(self, meta, *values):
        return GreaterExpr(values, meta.line, meta.column)
    def less_expr(self, meta, *values):
        return LessExpr(values, meta.line, meta.column)
    def greater_equal_expr(self, meta, *values):
        return GreaterEqualExpr(values, meta.line, meta.column)
    def less_equal_expr(self, meta, *values):
        return LessEqualExpr(values, meta.line, meta.column)
    def between(self, meta, left, right):
        return Between(left, right, meta.line, meta.column)
    def chance_percent(self, meta, value):
        return Chance(value, IntLiteral(100), meta.line, meta.column)
    def chance(self, meta, left, right):
        return Chance(left, right, meta.line, meta.column)
    def add(self, meta, left, right):
        return Add(left, right, meta.line, meta.column)
    def sub(self, meta, left, right):
        return Add(left, Neg(right), meta.line, meta.column)
    def mul(self, meta, left, right):
        return Mul(left, right, meta.line, meta.column)
    def div(self, meta, left, right):
        return Div(left, right, meta.line, meta.column)
    def pow(self, meta, left, right):
        return Pow(left, right, meta.line, meta.column)
    def neg(self, meta, value):
        return Neg(value, meta.line, meta.column)

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
    def call_expr(self, meta, *items):
        return Call(items)
    def args(self, meta, *items):
        return list(items)
    def params(self, meta, *items):
        return list(items)
    def list_item(self, meta, value):
        return value
    def NEWLINE(self, token):
        return Discard
    def INDENT(self, token):
        return Discard
    def DEDENT(self, token):
        return Discard