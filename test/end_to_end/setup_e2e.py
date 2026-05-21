import builtins, os, pytest

from src.ast import builder
from src.parser import parse
from src.visitors.interpreter.interpreter import InterpreterVisitor
# Raise the value if it's not a string, e.g. class (KeyboardInterrupt)
def fake_input(val):
    if not isinstance(val, str):
        raise val
    return val

def run_program(code, monkeypatch, capsys, inputs=None, slot=999):
    inputs = iter(inputs or [])
    monkeypatch.setattr(builtins, "input", lambda: fake_input(next(inputs)))

    tree = parse(code)
    ast = builder.ASTBuilder().transform(tree)

    interp = InterpreterVisitor(code, slot=slot)
    interp.run(ast)

    return capsys.readouterr().out.strip().splitlines()

@pytest.fixture(autouse=True)
def delete_save_file():
    yield
    try:
        os.remove(f"src/runtime/save_states/save_slot_999.json")
    except Exception as e:
        print("Error, when trying to delete a file:", e)