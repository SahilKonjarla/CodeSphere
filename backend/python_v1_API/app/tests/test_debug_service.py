import pytest
from unittest.mock import patch
from app.services.debug_service import process_debug_request

# Mock LangChain response for valid input
MOCK_LLM_RESPONSE = """
Issues:
- Syntax error on line 3.
Suggestions:
- Replace '=' with '==' for comparisons.
Explanation:
'=' is for assignment, '==' is for equality.
"""


@patch("app.services.debug_service.call_agent", return_value=MOCK_LLM_RESPONSE)
def test_process_debug_request_valid_code(mock_call_langchain):
    """
    Test process_debug_request with valid code.
    """
    code = "if x = 10: print(x)"

    # Call the function
    result = process_debug_request(code)

    # Assert the parsed output
    assert result["issues"] == ["Syntax error on line 3."]
    assert result["suggestions"] == ["Replace '=' with '==' for comparisons."]
    assert result["explanation"].startswith("'=' is for assignment")


def test_process_debug_request_empty_code():
    """
    Test process_debug_request with empty code input.
    """
    code = ""

    # Call the function and assert it raises a ValueError
    with pytest.raises(ValueError, match="Code snippet cannot be empty."):
        process_debug_request(code)


@patch("app.services.debug_service.call_agent", side_effect=Exception("Mock LLM error"))
def test_process_debug_request_langchain_error(mock_call_langchain):
    """
    Test process_debug_request when LangChain interaction fails.
    """
    code = "print('Hello World')"

    # Call the function and assert it raises a RuntimeError
    with pytest.raises(RuntimeError, match="Error communicating with the LLM: Mock LLM error"):
        process_debug_request(code)
