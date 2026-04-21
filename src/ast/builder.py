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
    def create_v(self, name, value=None):
        return CreateVariable(name, value)
    def create_s(self, name, struct_tail):
        return CreateStruct(name, struct_tail)
    def create_l(self, name, listing):
        return CreateList(name, listing)

    # tails
    def var_tail(self, value=None):
        return value
    def struct_tail(self, *items):
        return items
    def list_tail(self, value=None):
        return value

    # struct specifics
    def struct_fields(self, *items):
        return list(items)
    def struct_field(self, name, value=None):
        return CreateVariable(name, value)

    # list specifics
    def list_items(self, *values):
        return list(values)

    #Assignment
    def assign_v(self, name, base=None, value=None):
        return Assign(name, base, value)
    def assign_l(self, name, base=None, value=None):
        return Assign(name, base, value)
    def assign_i(self, name, base=None, value=None):
        return Assign(name, base, value)
    def assign_index(self, target, value, base=None):
            return Assign(target, base, value)
    
    #Reference used for assignment
    def reference(self, value, inheritance=None):
        if isinstance(value, str):
            return Var(value, inheritance)
        return value

    # general statements
    def if_stmt(self, cond, body, elifs=None, elses=None):
        return If(cond, body, elifs, elses)
    def elif_stmt(self, *items):
        return [items[i:i+2] for i in range(0, len(items), 2)]
    def else_stmt(self, item=None):
        return item
    def while_stmt(self, cond, body):
        return While(cond, body)
    def dowhile_stmt(self, body, cond):
        return Dowhile(body, cond)
    def forrange_stmt(self, name, start, end, body=None):
        return Forrange(name, start, end, body)
    def foreach_stmt(self, name, collection, body=None):
        return Foreach(name, collection, body)
    def func_def(self, name, params=None, body=None):
        return Define(name, params, body)
    def return_stmt(self, value):
        return Return(value)
    def break_stmt(self):
        return Break()
    def expr_stmt(self, value):
        return Expression(value)
    def input_stmt(self, value):
        return Input(value)
    def output_stmt(self, value):
        return Output(value)

    # EXPRESSIONS
    def or_expr(self, left, right):
        return OrExpr(left, right) 
    def and_expr(self, left, right):
        return AndExpr(left, right) 
    def either_expr(self, left, right):
        return XorExpr(left, right)
    def not_expr(self, cond):
        return NotExpr(cond) 
    def equal_expr(self, left, right):
        return EqualExpr(left, right)
    def not_equal_expr(self, left, right):
        return NotEqualExpr(left, right)
    def greater_expr(self, left, right):
        return GreaterExpr(left, right)
    def less_expr(self, left, right):
        return LessExpr(left, right)
    def greater_equal_expr(self, left, right):
        return GreaterEqualExpr(left, right)
    def less_equal_expr(self, left, right):
        return LessEqualExpr(left, right)
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
    def between(self, left, right):
        return Between(left, right)
    def chance_percent(self, value):
        return Chance(value, IntLiteral(100))
    def chance(self, left, right):
        return Chance(left, right)
    def var(self, name, base=None):
        return Var(name, base)
    def call_expr(self, name, args=None):
        return Call(name, args)
    def index_access(self, indexing, target, base):
        return IndexAccess(indexing, target, base)
    def indexing(self, *items):
        return list(items)
    def index_expr(self, value):
        return value

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
    def args(self, *items):
        return list(items)
    def params(self, *items):
        return list(items)
    def list_item(self, value):
        return value
    def inherits_from(sef, base):
        return base
    def inheritance(self, base=None):
        return base
    def more_stmt(self, *items):
        return list(items)
    def mul_stmt(self, *items):
        return list(items)
    def pos_stmt(self, item):
        return item
    def expr_list(self, *items):
        return list(items)
    def NEWLINE(self, token):
        return Discard
    def INDENT(self, token):
        return Discard
    def DEDENT(self, token):
        return Discard