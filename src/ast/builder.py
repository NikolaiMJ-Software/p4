from lark import Transformer, v_args
from lark import Discard

from src.ast.nodes import *

# AST BUILDER
@v_args(tree=True)  # tree instead of inline, because inline gives children directly but loses access to line + column
class ASTBuilder(Transformer):

    # positions important for positions for errors
    def _pos(self, node, tree):
        """Attach position from tree.meta to an AST node."""
        if hasattr(tree.meta, "line"):
            node.line = tree.meta.line
            node.column = tree.meta.column
        return node

    # from here on out, we'll manually extract children

    # START
    def start(self, tree):
        return tree.children

    # STATEMENTS
    # creates
    def create_v(self, tree):
        name = tree.children[0]
        value = tree.children[1] if len(tree.children) > 1 else None
        return self._pos(CreateVariable(name, value), tree)

    def create_s(self, tree):
        name = tree.children[0]
        struct_tail = tree.children[1]
        return self._pos(CreateStruct(name, struct_tail), tree)

    def create_l(self, tree):
        name = tree.children[0]
        value = tree.children[1] if len(tree.children) > 1 else None
        return self._pos(CreateList(name, value), tree)

    # tails
    def var_tail(self, tree):
        return tree.children[0] if tree.children else None

    def struct_tail(self, tree):
        return tuple(tree.children)

    def list_tail(self, tree):
        return tree.children[0] if tree.children else None

    # struct specifics
    def struct_fields(self, tree):
        return tree.children

    def struct_field(self, tree):
        name = tree.children[0]
        if len(tree.children) == 1: # if variable does not have value
            return self._pos(CreateVariable(name, None), tree)
        if isinstance(tree.children[1], list): # if variable has list value
            listing = tree.children[1]
            return self._pos(CreateList(name, listing), tree)
        value = tree.children[1] # otherwise, its variable with standard value
        return self._pos(CreateVariable(name, value), tree)

    # list specifics
    def list_items(self, tree):
        return tree.children

    # Assignment
    def assign_v(self, tree):
        name = tree.children[0]
        base = tree.children[1] if len(tree.children) > 2 else None
        value = tree.children[-1]
        return self._pos(Assign(name, base, value), tree)

    def assign_l(self, tree):
        name = tree.children[0]
        base = tree.children[1] if len(tree.children) > 2 else None
        value = tree.children[-1]
        return self._pos(Assign(name, base, value), tree)

    def assign_i(self, tree):
        name = tree.children[0]
        base = tree.children[1] if len(tree.children) > 2 else None
        value = tree.children[-1]
        return self._pos(Assign(name, base, value), tree)

    def assign_index(self, tree):
        target = tree.children[0]
        value = tree.children[1]
        return self._pos(AssignIndex(target, value), tree)

    # Reference used for assignment
    def reference(self, tree):
        value = tree.children[0]
        inheritance = tree.children[1] if len(tree.children) > 1 else None
        if isinstance(value, str):
            return Var(value, inheritance)
        return value

    # general statements
    def if_stmt(self, tree):
        cond = tree.children[0]
        body = tree.children[1]
        elifs = tree.children[2] if len(tree.children) > 2 else None
        elses = tree.children[3] if len(tree.children) > 3 else None
        return self._pos(If(cond, body, elifs, elses), tree)

    def elif_stmt(self, tree):
        items = tree.children
        return [items[i:i+2] for i in range(0, len(items), 2)]

    def else_stmt(self, tree):
        return tree.children[0] if tree.children else None

    def while_stmt(self, tree):
        cond = tree.children[0]
        body = tree.children[1]
        return self._pos(While(cond, body), tree)

    def dowhile_stmt(self, tree):
        body = tree.children[0]
        cond = tree.children[1]
        return self._pos(Dowhile(body, cond), tree)

    def forrange_stmt(self, tree):
        name = tree.children[0]
        start = tree.children[1]
        end = tree.children[2]
        body = tree.children[3] if len(tree.children) > 3 else None
        return self._pos(Forrange(name, start, end, body), tree)

    def foreach_stmt(self, tree):
        name = tree.children[0]
        collection = tree.children[1]
        body = tree.children[2] if len(tree.children) > 2 else None
        return self._pos(Foreach(name, collection, body), tree)

    def func_def(self, tree):
        name = tree.children[0]
        params = tree.children[1] if len(tree.children) > 1 else None
        body = tree.children[2] if len(tree.children) > 2 else None
        return self._pos(Define(name, params, body), tree)

    def return_stmt(self, tree):
        return self._pos(Return(tree.children[0]), tree)

    def break_stmt(self, tree):
        return self._pos(Break(), tree)

    def expr_stmt(self, tree):
        return self._pos(Expression(tree.children[0]), tree)

    def input_stmt(self, tree):
        return self._pos(Input(tree.children[0]), tree)

    def output_stmt(self, tree):
        return self._pos(Output(tree.children[0]), tree)

    # EXPRESSIONS
    def or_expr(self, tree):
        return self._pos(OrExpr(tree.children[0], tree.children[1]), tree)

    def and_expr(self, tree):
        return self._pos(AndExpr(tree.children[0], tree.children[1]), tree)

    def either_expr(self, tree):
        return self._pos(XorExpr(tree.children[0], tree.children[1]), tree)

    def not_expr(self, tree):
        return self._pos(NotExpr(tree.children[0]), tree)

    def equal_expr(self, tree):
        return self._pos(EqualExpr(tree.children[0], tree.children[1]), tree)

    def not_equal_expr(self, tree):
        return self._pos(NotEqualExpr(tree.children[0], tree.children[1]), tree)

    def greater_expr(self, tree):
        return self._pos(GreaterExpr(tree.children[0], tree.children[1]), tree)

    def less_expr(self, tree):
        return self._pos(LessExpr(tree.children[0], tree.children[1]), tree)

    def greater_equal_expr(self, tree):
        return self._pos(GreaterEqualExpr(tree.children[0], tree.children[1]), tree)

    def less_equal_expr(self, tree):
        return self._pos(LessEqualExpr(tree.children[0], tree.children[1]), tree)

    def add(self, tree):
        return self._pos(Add(tree.children[0], tree.children[1]), tree)

    def sub(self, tree):
        return self._pos(Add(tree.children[0], Neg(tree.children[1])), tree)

    def mul(self, tree):
        return self._pos(Mul(tree.children[0], tree.children[1]), tree)

    def div(self, tree):
        return self._pos(Div(tree.children[0], tree.children[1]), tree)

    def pow(self, tree):
        return self._pos(Pow(tree.children[0], tree.children[1]), tree)

    def neg(self, tree):
        return self._pos(Neg(tree.children[0]), tree)

    def between(self, tree):
        return self._pos(Between(tree.children[0], tree.children[1]), tree)

    def chance_percent(self, tree):
        return self._pos(Chance(tree.children[0], IntLiteral(100)), tree)

    def chance(self, tree):
        return self._pos(Chance(tree.children[0], tree.children[1]), tree)

    def var(self, tree):
        name = tree.children[0]
        base = tree.children[1] if len(tree.children) > 1 else None
        return self._pos(Var(name, base), tree)

    def call_expr(self, tree):
        name = tree.children[0]
        args = tree.children[1] if len(tree.children) > 1 else None
        return self._pos(Call(name, args), tree)

    def index_access(self, tree):
        indexing = tree.children[0]
        target = tree.children[1]
        base = tree.children[2] if len(tree.children) > 2 else None
        return self._pos(IndexAccess(indexing, target, base), tree)

    def indexing(self, tree):
        return tree.children

    def index_expr(self, tree):
        return tree.children[0]

    # TOKENS / helper rules
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

    def args(self, tree):
        return tree.children

    def params(self, tree):
        return tree.children

    def list_item(self, tree):
        return tree.children[0]

    def inherits_from(self, tree):
        return tree.children[0] if tree.children else None

    def inheritance(self, tree):
        return tree.children[0] if tree.children else None

    def more_stmt(self, tree):
        return tree.children

    def mul_stmt(self, tree):
        return tree.children

    def pos_stmt(self, tree):
        return tree.children[0]
    def expr_list(self, tree):
        return tree.children
    
    def NEWLINE(self, token):
        return Discard
    
    def INDENT(self, token):
        return Discard
    
    def DEDENT(self, token):
        return Discard