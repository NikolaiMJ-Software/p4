# function for making context
def make_context(code, line, column, context_lines=2):
    # find erroneous code snippet
    lines = code.splitlines()
    start = max(0, line - 1 - context_lines)
    end = min(len(lines), line + context_lines)
    snippet_lines = lines[start:end]
    
    # figure out which line in the snippet is the error line
    error_index = (line - 1) - start
    snippet_lines.insert(error_index + 1, " " * (column - 1) + "^")
    
    return "\n".join(snippet_lines)

# universal error class
class Error(Exception):
    def __init__(self, code, node, message):
        super().__init__(message)
        self.line = getattr(node, "line", None)     # getattr instead of self.line because
        self.column = getattr(node, "column", None) # it returns None if there's no line (doesn't crash)
        self.context = make_context(code, self.line, self.column) if code and self.line else None

# ignore this for now, could be used for semantic syntax errors later
# class SyntaxError(Error):
#     pass

class TypeError(Error):
    pass

class RuntimeError(Error):
    pass

class InterpreterError(Error):
    pass