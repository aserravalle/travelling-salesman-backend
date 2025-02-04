from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_assign_jobs():
    jobs = [
        {
            "id": 1,
            "date": "2025-02-05T09:00:00",
            "location": [40.7128, -74.0060],
            "duration": 60,
            "entry_time": "2025-02-05T09:00:00",
            "exit_time": "2025-02-05T12:00:00",
        }
    ]

    salesmen = [
        {
            "id": 101,
            "home_location": [40.730610, -73.935242],
            "start_time": "2025-02-05T09:00:00",
            "end_time": "2025-02-05T17:00:00",
        }
    ]

    response = client.post("/assign_jobs", json={"jobs": jobs, "salesmen": salesmen})

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "101" in response.json()
