from lark import Lark
from lark.indenter import Indenter
from lark.exceptions import UnexpectedInput

# GRAMMAR
grammar = r"""
start: stmt*
?stmt: create_stmt
    | assign_stmt
    | assign_index_stmt
    | if_stmt
    | while_stmt
    | dowhile_stmt
    | forrange_stmt
    | foreach_stmt
    | func_def
    | expr_stmt
    | input_stmt
    | output_stmt
    | NEWLINE


// EMPTY LINE STATEMENTS
create_stmt: "create" ID var_tail NEWLINE -> create_v
    | "create" ID struct_tail -> create_s
    | "create" ID "is" list_tail NEWLINE-> create_l

var_tail: ("is" expr)?

struct_tail: (inheritance "with:" NEWLINE INDENT struct_fields DEDENT | inherits_from)
struct_inheritance: "from" ID
struct_fields: (struct_field | NEWLINE)*
struct_field: ID NEWLINE
    | ID "is" expr NEWLINE
    | ID "is" "listing:" list_items? NEWLINE

list_tail: "listing:" list_items?
list_items: list_item ("," list_item)*

assign_stmt: ID inheritance "is" expr NEWLINE
    | ID inheritance "is" list_tail NEWLINE

assign_index_stmt: index_access "is" list_item NEWLINE-> assign_index

if_stmt: "if" expr "do:" NEWLINE block elif_stmt else_stmt
elif_stmt: ("else if" expr "do:" NEWLINE block)*
else_stmt: ("else do:" NEWLINE block)?

while_stmt: "while" expr "do:" NEWLINE block

dowhile_stmt: "do:" NEWLINE block "while" expr NEWLINE

forrange_stmt: "for each" ID "from" expr "to" expr "do:" NEWLINE block

foreach_stmt: "for each" ID "in" ID "do:" NEWLINE block

func_def: "define" ID params ":" NEWLINE block
params: ("with" ID ("," ID)*)?

expr_stmt: expr NEWLINE

input_stmt: "input in" indexing ID inheritance? NEWLINE

output_stmt: "output" expr_list NEWLINE
expr_list: expr ("," expr)*


// BLOCK STATEMENTS
return_stmt: "return" expr NEWLINE

break_stmt: "stop" NEWLINE


// EXPRESSIONS
?expr: expr2
    | expr "or" expr2 -> or_expr
    | "either" expr2 "or" expr2 -> either_expr
?expr2: expr3
    | expr2 "and" expr3 -> and_expr
?expr3: expr4
    | "not" expr4 -> not_expr
?expr4: expr5
    | expr5 "equal" expr5 -> equal_expr
    | expr5 "not equal" expr5 -> not_equal_expr
    | expr5 "greater than" expr5 -> greater_expr
    | expr5 "less than" expr5 -> less_expr
    | expr5 "greater than or equal to" expr5 -> greater_equal_expr
    | expr5 "less than or equal to" expr5 -> less_equal_expr
?expr5: expr6
    | expr5 "+" expr6 -> add
    | expr5 "-" expr6 -> sub
?expr6: expr7
    | expr6 "*" expr7 -> mul
    | expr6 "/" expr7 -> div
?expr7: expr8
    | expr8 "^" expr7 -> pow
?expr8: "-" expr8 -> neg
    | "between" expr5 "and" expr5 -> between
    | "chance" expr "%" -> chance_percent
    | "chance" expr "in" expr -> chance
    | "(" expr ")"
    | INTEGER
    | FLOAT
    | STRING
    | BOOL
    | ID inheritance -> var
    | call_expr
    | index_access -> index_expr


// TOKENS
ID: /[A-Z][a-zA-Z0-9_]*/
FLOAT: /([1-9][0-9]*|0)\.[0-9]+/
INTEGER: /[0-9]+/
STRING: /"[^"]*"/
BOOL: "true"|"false"


// GENERAL HELPER RULES
call_expr: "call" ID args -> call_expr
args: ("with" expr ("," expr)*)?
inherits_from: "from" ID
inheritance: ("from" ID)?
block: INDENT (stmt | break_stmt | return_stmt)+ DEDENT
list_item: expr | list_tail
indexing: ("index" expr "of")*
index_access: indexing ID inheritance


// IMPORTS & IGNORE
NEWLINE: (/\r?\n[ \t]*/)
%import common.WS_INLINE
%declare INDENT DEDENT
%ignore WS_INLINE


// COMMENTS
COMMENT: /\#[^\n]*/
BLOCK_COMMENT: /\#\/[\s\S]*?\/\#/
%ignore COMMENT
%ignore BLOCK_COMMENT
"""



class TreeIndenter(Indenter):
    NL_type = 'NEWLINE'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = 'INDENT'
    DEDENT_type = 'DEDENT'
    tab_len = 8


# PARSER
parser = Lark(
    grammar,
    parser="lalr",
    start="start",
    postlex=TreeIndenter(),
    propagate_positions=True
)


# wrapping Lark errors in our own (decouples us from Lark)
class ParseError(Exception):
    def __init__(self, message, line, column, context):
        super().__init__(message)
        self.line = line
        self.column = column
        self.context = context


# raising our own wrapped errors while parsing
def parse(code):
    try:
        if not code.endswith("\n"):
            code += "\n"
        check_keyword_caps(code)
        return parser.parse(code)
    except UnexpectedInput as e:
        raise ParseError( # raise error with line + column + context from caught exception
            "Syntax error",
            e.line,
            e.column,
            e.get_context(code)
        )
  

# error message helper function
def check_keyword_caps(code):
    # Define keywords which must be lowercase
    keywords = {
        "create", "define", "if", "else", "while",
        "do", "for", "output", "input",
        "return", "stop", "call"
    }

    #go through each line and its line numbers
    for line_no, line in enumerate(code.splitlines(), start=1):
        #strip white space from line
        stripped = line.lstrip()
        # Initial column position after indentation
        column = len(line) - len(stripped) + 1

        #if line empty, ignore it
        if not stripped:
            continue

        # Split line into tokens
        tokens = [t.rstrip(":") for t in stripped.split()]

        #check if token is one of the keywords but not lowercase
        for token in tokens:
            if token.lower() in keywords and token not in keywords:

                column = line.index(token) + 1
                # Create error context with pointer
                context = line + "\n" + " " * (column - 1) + "^"

                raise ParseError(
                    f"Unknown keyword: '{token}'. Did you mean '{token.lower()}'?",
                    line_no,
                    column,
                    context
                )