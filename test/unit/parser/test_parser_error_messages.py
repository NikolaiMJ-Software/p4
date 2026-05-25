import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

import pytest
from src.parser import parse, ParseError

#################
# Error Message #
#################
 
def test_parser_rejects_capitalized_keyword():
    with pytest.raises(ParseError) as exc_info:
        parse("Create X is 5\n")

    error = exc_info.value

    assert error.line == 1
    assert error.column == 1
    assert "Unknown keyword: 'Create'. Did you mean 'create'?" in str(error)
    assert "^" in error.context

def test_parser_rejects_capitalized_inline_keyword():
    with pytest.raises(ParseError) as exc_info:
        parse('while true Do:\n    output "hej"\n')

    error = exc_info.value

    assert error.line == 1
    assert error.column == 12
    assert "Unknown keyword: 'Do'. Did you mean 'do'?" in str(error)
    assert "^" in error.context