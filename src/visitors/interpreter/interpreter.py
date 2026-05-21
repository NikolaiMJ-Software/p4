from .runtime_value import RuntimeValue
from src.visitors.base_visitor import Visitor
from src.ast.nodes import *
from src.runtime.game_state import GameStateManager
from src.visitors.type_checker import *
from src.errors import InterpreterError
from src.errors import TypeError as TypeCheckError
from .exceptions import ReturnException, BreakException

from .arithmetic import Arithmetic
from .variables import Variables
from .functions import Functions
from .control_flow import ControlFlow
from .loops import Loops
from .lists import Lists
from .structs import Structs
from .game_state import GameState
from .boolean import Boolean
from .comparison import Comparison


# INTERPRETER
class InterpreterVisitor(
    Visitor,
    Arithmetic,
    Boolean,
    Comparison,
    Variables,
    Functions,
    ControlFlow,
    Loops,
    Lists,
    Structs,
    GameState,
):
    def __init__(self, code="", slot=1):
        self.code = code
        self.v_table = {}
        self.f_table = {}
        self.game_state_manager = GameStateManager(slot)
        self.type_checker = TypeChecker(self.code)

    # SCOPE HANDLING
    def lookup_var(self, name):
        scope = self.v_table
        while scope:
            if name in scope:
                return scope[name]
            scope = scope.get("__parent__")
        return False

    def lookup_fun(self, name):
        scope = self.f_table
        while scope:
            if name in scope:
                return scope[name]
            scope = scope.get("__parent__")
        return False

    # UNWRAPPING OF RUNTIMEVALUES
    def unwrap(self, value):
        if isinstance(value, RuntimeValue):
            return value.value
        return value

    def unwrap_list(self, input_list):
        var_list = []
        for var in input_list:
            if isinstance(var, list):
                var_list.append(self.unwrap_list(var))
            else:
                var_list.append(self.unwrap(var))
        return var_list

    # MAIN RUN
    def run(self, ast):
        should_save = True

        try:
            for stmt in ast:
                self.visit(stmt)

            self.load_game_state()

            if "Play" in self.f_table:
                self.visit(Call("Play", []))

        except KeyboardInterrupt:
            print("\nProgram interrupted. Saving game state...")

        except (InterpreterError, TypeCheckError):
            should_save = False
            raise

        finally:
            if should_save:
                self.save_game_state()

    # LITERALS
    def visit_int_literal(self, node):
        return RuntimeValue("int", node.value)

    def visit_float_literal(self, node):
        return RuntimeValue("float", node.value)

    def visit_string_literal(self, node):
        return RuntimeValue("str", node.value)

    def visit_bool_literal(self, node):
        return RuntimeValue("bool", node.value)

    def visit_expression(self, node):
        return self.visit(node.value)