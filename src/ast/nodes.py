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


# STATEMENTS
class CreateVariable(ASTNode):
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
    def __repr__(self):
        return f"Create_v({self.name},{self.value})" 
class CreateStruct(ASTNode):
    def __init__(self, name, struct_tail):
        self.name = name
        self.base = struct_tail[0]
        self.fields = struct_tail[1]
    def __repr__(self):
        return f"Create_s({self.name},{self.base},{self.fields})"
class CreateList(ASTNode):
    def __init__(self, name, listing):
        self.name = name
        self.listing = listing
    def __repr__(self):
        return f"Create_l({self.name},{self.listing})"
class Assign(ASTNode):
    def __init__(self, name, base, value):
        self.name = name
        self.base = base
        self.value = value
    def __repr__(self):
        return f"Assign({self.name},{self.base},{self.value})"
class AssignIndex(ASTNode):
    def __init__(self, target, value):
        self.target = target
        self.value = value
    def __repr__(self):
        return f"AssignIndex({self.target},{self.value})"
class If(ASTNode):
    def __init__(self, cond, body, elifs, elses):
        self.cond = cond
        self.body = body
        self.elifs = elifs
        self.elses = elses
    def __repr__(self):
        return f"If({self.cond},{self.body},{self.elifs},{self.elses})"
class While(ASTNode):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body
    def __repr__(self):
        return f"While({self.cond},{self.body})"
class Dowhile(ASTNode):
    def __init__(self, body, cond):
        self.body = body
        self.cond = cond
    def __repr__(self):
        return f"Dowhile({self.body},{self.cond})"
class Forrange(ASTNode):
    def __init__(self, name, start, end, body):
        self.name = name
        self.start = start
        self.end = end
        self.body = body
    def __repr__(self):
        return f"Forrange({self.name},{self.start},{self.end},{self.body})"
class Foreach(ASTNode):
    def __init__(self, name, collection, body):
        self.name = name
        self.collection = collection
        self.body = body
    def __repr__(self):
        return f"Foreach({self.name},{self.collection},{self.body})"
class Define(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body
    def __repr__(self):
        return f"Define({self.name},{self.params},{self.body})"
class Return(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Return({self.value})"
class Break(ASTNode):
    def __repr__(self):
        return "Break()"
class Expression(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Expr({self.value})"
class Input(ASTNode):
    def __init__(self, value):
        self.name = value
    def __repr__(self):
        return f"Input({self.name})"
class Output(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Output({self.value})"


# EXPRESSIONS
class OrExpr(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Or({self.left},{self.right})"
class AndExpr(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"And({self.left},{self.right})"
class XorExpr(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Xor({self.left},{self.right})"
class NotExpr(ASTNode):
    def __init__(self, cond):
        self.cond = cond
    def __repr__(self):
        return f"Not({self.cond})"
class EqualExpr(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Equal({self.left},{self.right})"
class NotEqualExpr(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"NotEqual({self.left},{self.right})"
class GreaterExpr(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Greater({self.left},{self.right})"
class LessExpr(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Less({self.left},{self.right})"
class GreaterEqualExpr(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"GreaterEqual({self.left},{self.right})"
class LessEqualExpr(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"LessEqual({self.left},{self.right})"  
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
class Neg(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Neg({self.value})"
class Between(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Between({self.left},{self.right})"
class Chance(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Chance({self.left},{self.right})"
class Var(ASTNode):
    def __init__(self, name, base=None):
        self.name = name
        self.base = base
    def __repr__(self):
        return f"Var({self.name},{self.base})"
class Call(ASTNode):
    def __init__(self, name, args=None):
        self.name = name
        self.args = args
    def __repr__(self):
        return f"Call({self.name},{self.args})"
class IndexAccess(ASTNode):
    def __init__(self, indexing, target, base):
        self.indexing = indexing
        self.target = target
        self.base = base
    def __repr__(self):
        return f"IndexAccess({self.indexing},{self.target},{self.base})"
