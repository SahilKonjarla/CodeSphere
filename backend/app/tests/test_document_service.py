import pytest
from unittest.mock import patch
from app.services.document_service import (
    process_docstring_request,
    process_comments_request,
    process_overview_request,
    process_readme_request,
)

# Mock responses for each route
MOCK_DOCSTRING_RESPONSE = """
Adds two numbers.

Args:
    a (int): The first number.
    b (int): The second number.

Returns:
    int: The sum of a and b.
"""

MOCK_COMMENTS_RESPONSE = """
# This function takes two arguments, a and b.
# It returns their sum.
"""

MOCK_OVERVIEW_RESPONSE = """
This code defines a function `add` that takes two arguments and returns their sum.
It is a simple implementation of an addition operation.
"""

MOCK_README_RESPONSE = """
# Simple Addition Function

## Purpose
This Python script defines a simple function `add` that adds two numbers and returns their sum.

## Usage
To use this function, call `add(a, b)` with two numerical arguments:
```python
result = add(5, 3)
print(result)  # Output: 8
"""


@patch("app.services.document_service.call_agent", return_value=MOCK_DOCSTRING_RESPONSE)
def test_generate_docstring_valid_code(mock_call_langchain):
    """
    Test generate_docstring with valid code input.
    """
    code = "def add(a, b): return a + b"

    result = process_docstring_request(code)

    assert result.startswith("Adds two numbers.")
    assert "Args:" in result
    assert "Returns:" in result


def test_generate_docstring_empty_code():
    """
    Test generate_docstring with empty code input.
    """
    code = ""

    with pytest.raises(ValueError, match="Code snippet cannot be empty."):
        process_docstring_request(code)


@patch("app.services.document_service.call_agent", side_effect=Exception("LangChain API error"))
def test_generate_docstring_langchain_error(mock_call_langchain):
    """
    Test generate_docstring when LangChain interaction fails.
    """
    code = "def add(a, b): return a + b"

    with pytest.raises(RuntimeError, match="Error communicating with the LLM: LangChain API error"):
        process_docstring_request(code)


@patch("app.services.document_service.call_agent", return_value=MOCK_COMMENTS_RESPONSE)
def test_generate_comments_valid_code(mock_call_langchain):
    """
    Test generate_comments with valid code input.
    """
    code = "def add(a, b): return a + b"

    result = process_comments_request(code)

    assert result.startswith("# This function takes two arguments")
    assert "It returns their sum." in result


def test_generate_comments_empty_code():
    """
    Test generate_comments with empty code input.
    """
    code = ""

    with pytest.raises(ValueError, match="Code snippet cannot be empty."):
        process_comments_request(code)


@patch("app.services.document_service.call_agent", side_effect=Exception("LangChain API error"))
def test_generate_comments_langchain_error(mock_call_langchain):
    """
    Test generate_comments when LangChain interaction fails.
    """
    code = "def add(a, b): return a + b"

    with pytest.raises(RuntimeError, match="Error communicating with the LLM: LangChain API error"):
        process_comments_request(code)


@patch("app.services.document_service.call_agent", return_value=MOCK_OVERVIEW_RESPONSE)
def test_generate_overview_valid_code(mock_call_langchain):
    """
    Test generate_overview with valid code input.
    """
    code = "def add(a, b): return a + b"

    result = process_overview_request(code)

    assert result.startswith("This code defines a function")
    assert "It is a simple implementation" in result


def test_generate_overview_empty_code():
    """
    Test generate_overview with empty code input.
    """
    code = ""

    with pytest.raises(ValueError, match="Code snippet cannot be empty."):
        process_overview_request(code)


@patch("app.services.document_service.call_agent", side_effect=Exception("LangChain API error"))
def test_generate_overview_langchain_error(mock_call_langchain):
    """
    Test generate_overview when LangChain interaction fails.
    """
    code = "def add(a, b): return a + b"

    with pytest.raises(RuntimeError, match="Error communicating with the LLM: LangChain API error"):
        process_overview_request(code)


@patch("app.services.document_service.call_agent", return_value=MOCK_OVERVIEW_RESPONSE)
def test_generate_readme_valid_code(mock_call_langchain):
    """
    Test generate_overview with valid code input.
    """
    code = "def add(a, b): return a + b"

    result = process_readme_request(code)

    assert result.startswith("This code defines a function")
    assert "It is a simple implementation" in result


def test_generate_readme_empty_code():
    """
    Test generate_overview with empty code input.
    """
    code = ""

    with pytest.raises(ValueError, match="Code snippet cannot be empty."):
        process_readme_request(code)


@patch("app.services.document_service.call_agent", side_effect=Exception("LangChain API error"))
def test_generate_readme_langchain_error(mock_call_langchain):
    """
    Test generate_overview when LangChain interaction fails.
    """
    code = "def add(a, b): return a + b"

    with pytest.raises(RuntimeError, match="Error communicating with the LLM: LangChain API error"):
        process_readme_request(code)
