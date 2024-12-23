from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_debug_route_valid_input():
    """
    Test /debug with valid input.
    """
    payload = {
        "code": "if x = 10: print(x)"
    }

    response = client.post("/debug", json=payload)

    # Assert response status and content
    assert response.status_code == 200
    data = response.json()
    assert "issues" in data
    assert "suggestions" in data
    assert "explanation" in data


def test_debug_route_missing_code():
    """
    Test /debug with missing code field.
    """
    payload = {
    }

    response = client.post("api/v1/debug", json=payload)

    # Assert validation error (422 Unprocessable Entity)
    assert response.status_code == 422
    assert "detail" in response.json()


def test_debug_route_service_error():
    """
    Test /debug when the service layer raises an error.
    """
    # Mock the service to raise an error
    with patch("app.services.debug_service.process_debug_request", side_effect=RuntimeError("Service error")):
        payload = {
            "code": "print('Hello World')"
        }

        response = client.post("api/v1/debug", json=payload)

        # Assert internal server error (500)
        assert response.status_code == 500
        assert "detail" in response.json()
        assert response.json()["detail"] == "An error occurred while processing your request."
