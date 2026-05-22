from src.errors import TypeError

from .arithmetic import Arithmetic
from .boolean import Boolean
from .comparison import Comparison
from .control_flow import ControlFlow
from .functions import Functions
from .game_state import GameState
from .lists import Lists
from .structs import Structs
from .variables import Variables


class TypeChecker(
    Arithmetic,
    Boolean,
    Comparison,
    Variables,
    Functions,
    ControlFlow,
    Lists,
    Structs,
    GameState,
):
    def __init__(self, code=""):
        self.code = code