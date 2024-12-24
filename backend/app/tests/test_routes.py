from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_debug_route_valid_input():
    """
    Test /debug with valid input.
    """
    payload = {
        "code": "if x = 10: print(x)",
    }

    response = client.post("api/v1/debug", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "issues" in data
    assert "suggestions" in data
    assert "explanation" in data


def test_optimize_route_valid_input():
    """
    Test /optimize with valid input.
    """
    payload = {
        "code": "for i in range(100): print(i)",
        "goal": "performance"
    }

    response = client.post("api/v1/optimize", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "inefficiencies" in data
    assert "suggestions" in data
    assert "explanation" in data


def test_optimize_route_missing_code():
    """
    Test /optimize with missing code field.
    """
    payload = {
        "goal": "performance"
    }

    response = client.post("api/v1/optimize", json=payload)

    assert response.status_code == 422
    assert "detail" in response.json()


def test_optimize_route_service_error(mocker):
    """
    Test /optimize when the service layer raises an error.
    """
    # Mock the service to raise a RuntimeError
    mocker.patch(
        "app.services.optimize_service.process_optimization_request",
        side_effect=RuntimeError("Mocked service error")
    )

    payload = {
        "code": "for i in range(100): print(i)",
        "goal": "performance"
    }

    response = client.post("api/v1/optimize", json=payload)

    assert response.status_code == 500
    assert response.json()["detail"] == "An internal error occurred while processing the optimization request."
