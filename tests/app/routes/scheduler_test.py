from fastapi.testclient import TestClient
from app.main import app  # Import your FastAPI app

client = TestClient(app)  # Simulates an API client


def test_schedule_endpoint():
    request_data = {
        "jobs": [
            {"property_id": 1, "duration": 90, "time_window": "ENTRADA"},
            {"property_id": 2, "duration": 60, "time_window": "SALIDA"},
        ],
        "cleaners": [
            {
                "cleaner_id": 101,
                "name": "John",
                "hours_available": 8,
                "home_address": "Valencia",
            },
            {
                "cleaner_id": 102,
                "name": "Jane",
                "hours_available": 8,
                "home_address": "Valencia",
            },
        ],
    }

    response = client.post("/schedule/", json=request_data)

    assert response.status_code == 200
    assert "schedule" in response.json()
    assert isinstance(response.json()["schedule"], list)
    assert len(response.json()["schedule"]) == 2


def test_schedule_endpoint_invalid_data():
    bad_request_data = {
        "jobs": [],  # No jobs provided
        "cleaners": [
            {
                "cleaner_id": 101,
                "name": "John",
                "hours_available": 8,
                "home_address": "Valencia",
            }
        ],
    }

    response = client.post("/schedule/", json=bad_request_data)

    assert response.status_code == 422  # Unprocessable Entity
    assert (
        "detail" in response.json()
    )  # FastAPI includes validation details in the response
