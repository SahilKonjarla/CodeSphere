import pytest
from unittest.mock import patch
from app.services.learner_service import process_learner_request

# Mock database logs for valid input
MOCK_PARSED_LOGS = [
    {
        "agent": "debugging",
        "code": "for i in range(10): print(i)",
        "errors": ["Syntax error"],
        "suggestions": ["Replace '=' with '=='"],
        "explanation": "The '=' operator is invalid in this context.",
        "timestamp": "2024-12-22T15:30:00Z"
    },
    {
        "agent": "optimization",
        "code": "def add(a, b): return a + b",
        "inefficiencies": ["Inefficient loop"],
        "suggestions": ["Use a generator expression"],
        "explanation": "Using a generator is more memory-efficient.",
        "timestamp": "2024-12-22T16:00:00Z"
    }
]

# Mock LangChain response
MOCK_LLM_RESPONSE = """
Trends:
- Frequent syntax errors in Python loops.
- Common requests for performance optimizations.
Recommendations:
- Use `flake8` for linting Python code.
- Learn about generator expressions to optimize loops.
Resources:
- [Python Linting with Flake8](https://flake8.pycqa.org)
- [Guide to Python Generators](https://realpython.com/introduction-to-python-generators/)
"""


@patch("app.services.learner_service.call_agent", return_value=MOCK_LLM_RESPONSE)
def test_process_learner_request_valid_logs(mock_call_agent):
    """
    Test process_learner_request with valid logs.
    """
    user_id = "123"

    # Mock fetch_recent_logs to return parsed logs
    with patch("app.services.learner_service.fetch_recent_logs", return_value=MOCK_PARSED_LOGS):
        # Call the function
        result = process_learner_request(user_id)

    # Assert the parsed output
    assert "Trends" in result
    assert "Recommendations" in result
    assert "Resources" in result
    assert "Frequent syntax errors" in result["Trends"]
    assert "Use `flake8` for linting" in result["Recommendations"]


def test_process_learner_request_no_logs():
    """
    Test process_learner_request with no logs.
    """
    user_id = "123"

    # Mock fetch_recent_logs to return an empty list
    with patch("app.services.learner_service.fetch_recent_logs", return_value=[]):
        # Call the function and assert it raises a ValueError
        with pytest.raises(ValueError, match="No recent logs found for the user."):
            process_learner_request(user_id)


@patch("app.services.learner_service.call_agent", side_effect=Exception("Mock LLM error"))
def test_process_learner_request_langchain_error(mock_call_agent):
    """
    Test process_learner_request when LangChain interaction fails.
    """
    user_id = "123"

    # Mock fetch_recent_logs to return parsed logs
    with patch("app.services.learner_service.fetch_recent_logs", return_value=MOCK_PARSED_LOGS):
        # Call the function and assert it raises a RuntimeError
        with pytest.raises(RuntimeError, match="Error communicating with the Learner Agent: Mock LLM error"):
            process_learner_request(user_id)
