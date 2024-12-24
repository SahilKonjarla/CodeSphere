import pytest
from unittest.mock import patch
from app.services.optimize_service import process_optimization_request

MOCK_OPTIMIZE_RESPONSE = """
Inefficiencies:
1. Inefficient loop structure detected.
Suggestions:
1. Replace the loop with a generator expression to reduce memory usage.
Explanation:
The current implementation iterates through a large range and stores results unnecessarily. A generator expression is more memory-efficient.
"""


@patch("app.services.optimize_service.call_langchain", return_value=MOCK_OPTIMIZE_RESPONSE)
def test_process_optimization_request_valid_code(mock_call_langchain):
    """
    Test process_optimization_request with valid code input.
    """
    code = "for i in range(100): print(i)"
    language = "python"
    goal = "performance"

    result = process_optimization_request(code, language, goal)

    assert result["inefficiencies"] == ["Inefficient loop structure detected."]
    assert result["suggestions"] == ["Replace the loop with a generator expression to reduce memory usage."]
    assert result["explanation"].startswith("The current implementation iterates")


def test_process_optimization_request_empty_code():
    """
    Test process_optimization_request with empty code input.
    """
    code = ""
    language = "python"
    goal = "performance"

    with pytest.raises(ValueError, match="Code snippet cannot be empty."):
        process_optimization_request(code, language, goal)


@patch("app.services.optimize_service.call_langchain", side_effect=Exception("LangChain API error"))
def test_process_optimization_request_langchain_error(mock_call_langchain):
    """
    Test process_optimization_request when LangChain interaction fails.
    """
    code = "for i in range(100): print(i)"
    language = "python"
    goal = "performance"

    with pytest.raises(RuntimeError, match="Error communicating with the LLM: LangChain API error"):
        process_optimization_request(code, language, goal)
