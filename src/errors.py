from lark import Lark

#class for finding specific line number span
class SourceSpan:
    def __init__(self, line, column, end_line=None, end_column=None):
        self.line = line                        # line number (1-indexed)
        self.column = column                    # column number (0-indexed)
        self.end_line = end_line or line
        self.end_column = end_column or column
    
    def __repr__(self):
        return f"SourceSpan({self.line}:{self.column})"

#class for diagnostic (type of error)
class Diagnostic:
    def _init_(self, kind, message, span, hint=None):
        self.kind = kind            # "SyntaxError", "TypeError", "RuntimeError"
        self.message = message      # human-readable error message
        self.span = span            # line numbers/span of the error
        self.hint = hint            # optional help text

    def __repr__(self):
        return f"{self.kind} at {self.span}: {self.message}"
    
#uses diagnostic string for Exception (built in error messages in Python)
class LangError(Exception):
    def _init_(self, diagnostic):
        self.diagnostic = diagnostic
        super().__init__(str(diagnostic))