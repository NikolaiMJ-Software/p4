# CLASSES FOR AST
import re
class ASTNode:
    def __init__(self, line = None, column = None):
        self.line = line
        self.column = column
    
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

## BoolOp classes
class OrExpr(ASTNode):
    def __init__(self, values, line=None, column=None):
        super().__init__(line, column)
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"Or({self.cond},{self.cond2})"
class AndExpr(ASTNode):
    def __init__(self, values, line=None, column=None):
        super().__init__(line, column)
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"And({self.cond},{self.cond2})"
class XorExpr(ASTNode):
    def __init__(self, values, line=None, column=None):
        super().__init__(line, column)
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"Xor({self.cond},{self.cond2})"
class NotExpr(ASTNode):
    def __init__(self, value, line=None, column=None):
        super().__init__(line, column)
        self.cond = value
    def __repr__(self):
        return f"Not({self.cond})"
class EqualExpr(ASTNode):
    def __init__(self, values, line=None, column=None):
        super().__init__(line, column)
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"Equal({self.cond},{self.cond2})"
class NotEqualExpr(ASTNode):
    def __init__(self, values, line=None, column=None):
        super().__init__(line, column)
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"NotEqual({self.cond},{self.cond2})"
class GreaterExpr(ASTNode):
    def __init__(self, values, line=None, column=None):
        super().__init__(line, column)
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"Greater({self.cond},{self.cond2})"
class LessExpr(ASTNode):
    def __init__(self, values, line=None, column=None):
        super().__init__(line, column)
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"Less({self.cond},{self.cond2})"
class GreaterEqualExpr(ASTNode):
    def __init__(self, values, line=None, column=None):
        super().__init__(line, column)
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"GreaterEqual({self.cond},{self.cond2})"
class LessEqualExpr(ASTNode):
    def __init__(self, values, line=None, column=None):
        super().__init__(line, column)
        self.cond = values[0]
        self.cond2 = values[1]
    def __repr__(self):
        return f"LessEqual({self.cond},{self.cond2})"
# STATEMENTS

# creates
class Create_v(ASTNode):
    def __init__(self, values):
        self.name = values[0]
        self.value = values[1] if len(values) > 1 else None
    def __repr__(self):
        return f"Create_v({self.name},{self.value})"
        
class Create_s(ASTNode): # struct creation
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

class Create_l(ASTNode): # list creation
    def __init__(self, values): # receives name + list (values)
        self.name = values[0] # first (values[0]) is always name
        self.listing = values[1] # 1: means from 1 and onwards
    def __repr__(self):
        return f"Create_l({self.name},{self.listing})"
    
class Define(ASTNode):
    def __init__(self, items, line=None, column=None):
        super().__init__(line, column)
        self.name = items[0]
        if isinstance(items[1], list):
            params = items[1]
            body = items[2]
        else:
            params = []
            body = list(items[1:])
        self.params = params or []
        self.body = body or []
    def __repr__(self):
        return f"Define({self.name},{self.params},{self.body})"
class If(ASTNode):
    def __init__(self, cond, body, else_body=None, line=None, column=None):
        super().__init__(line, column)
        self.cond = cond
        self.body = body
        self.else_body = else_body
    def __repr__(self):
        return f"If({self.cond},{self.body},{self.else_body})"
class While(ASTNode):
    def __init__(self, values, line=None, column=None):
        super().__init__(line, column)
        self.cond = values[0]
        self.body = list(values[1:])
    def __repr__(self):
        return f"While({self.cond},{self.body})"
class Dowhile(ASTNode):
    def __init__(self, values, line=None, column=None):
        super().__init__(line, column)
        self.body = list(values[:-1])
        self.cond = values[-1]
    def __repr__(self):
        return f"Dowhile({self.body},{self.cond})"
class Forrange(ASTNode):
    def __init__(self, values, line=None, column=None):
        super().__init__(line, column)
        self.name = values[0]
        self.start = values[1]
        self.end = values[2]
        self.body = list(values[3:])
    def __repr__(self):
        return f"Forrange({self.name},{self.start},{self.end},{self.body})"
class Foreach(ASTNode):
    def __init__(self, values, line=None, column=None):
        super().__init__(line, column)
        self.name = values[0]
        self.collection = values[1]
        self.body = list(values[2:])
    def __repr__(self):
        return f"Foreach({self.name},{self.collection},{self.body})"
class Return(ASTNode):
    def __init__(self, value, line=None, column=None):
        super().__init__(line, column)
        self.value = value
    def __repr__(self):
        return f"Return({self.value})"
class Expression(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Expr({self.value})"
class Input(ASTNode):
    def __init__(self, value, line=None, column=None):
        super().__init__(line, column)
        self.name = value
    def __repr__(self):
        return f"Input({self.name})"
class Output(ASTNode):
    def __init__(self, value, line=None, column=None):
        super().__init__(line, column)
        self.name = value
    def __repr__(self):
        return f"Output({self.name})"
class Assign(ASTNode):
    def __init__(self, values, line=None, column=None):
        super().__init__(line, column)
        self.name = values[0]
        self.value = values[1]
    def __repr__(self):
        return f"Assign({self.name} is {self.value})"
class Between(ASTNode):
    def __init__(self, left, right, line=None, column=None):
        super().__init__(line, column)
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Between({self.left},{self.right})"
class Chance(ASTNode):
    def __init__(self, left, right, line=None, column=None):
        super().__init__(line, column)
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Chance({self.left},{self.right})"
class Add(ASTNode):
    def __init__(self, left, right, line=None, column=None):
        super().__init__(line, column)
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Add({self.left},{self.right})"
class Mul(ASTNode):
    def __init__(self, left, right, line=None, column=None):
        super().__init__(line, column)
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Mul({self.left},{self.right})"
class Div(ASTNode):
    def __init__(self, left, right, line=None, column=None):
        super().__init__(line, column)
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Div({self.left},{self.right})"
class Pow(ASTNode):
    def __init__(self, left, right, line=None, column=None):
        super().__init__(line, column)
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Pow({self.left},{self.right})"
class Neg(ASTNode):
    def __init__(self, value, line=None, column=None):
        super().__init__(line, column)
        self.value = value
    def __repr__(self):
        return f"Neg({self.value})"
class Call(ASTNode):
    def __init__(self, values, line=None, column=None):
        super().__init__(line, column)
        self.name = values[0]
        self.args = list(values[1])
    def __repr__(self):
        return f"Call({self.name},{self.args})"