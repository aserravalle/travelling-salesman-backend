from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_assign_jobs_api():
    # Test job data
    request = {
        "jobs": [
            {
                "job_id": "1",
                "date": "2025-02-05T09:00:00",
                "location": [40.7128, -74.0060],
                "duration_mins": 60,
                "entry_time": "2025-02-05T09:00:00",
                "exit_time": "2025-02-05T12:00:00",
            },
            {
                "job_id": "2",
                "date": "2025-02-05T10:00:00",
                "location": [40.7130, -74.0055],
                "duration_mins": 45,
                "entry_time": "2025-02-05T10:30:00",
                "exit_time": "2025-02-05T14:00:00",
            },
        ],
        "salesmen": [
            {
                "salesman_id": "101",
                "home_location": [40.730610, -73.935242],
                "start_time": "2025-02-05T09:00:00",
                "end_time": "2025-02-05T17:00:00",
            },
            {
                "salesman_id": "102",
                "home_location": [40.750610, -73.975242],
                "start_time": "2025-02-05T09:00:00",
                "end_time": "2025-02-05T17:00:00",
            },
        ],
    }

    # Send request to API
    response = client.post("/assign_jobs", json=request)

    # ✅ Validate response status
    assert response.status_code == 200, "Response should have status 200"

    # ✅ Validate response structure
    response_json = response.json()
    assert isinstance(response_json, dict), "Response should be a dictionary"
    assert "roster_id" in response_json, "Response should contain 'roster_id'"
    assert "date" in response_json, "Response should contain 'date'"
    assert "jobs" in response_json, "Response should contain 'jobs'"

    # ✅ Validate jobs are assigned
    assigned_jobs = response_json["jobs"]
    assert isinstance(assigned_jobs, dict), "Jobs should be returned as a dictionary"

    # Ensure salesman IDs are **strings** in the JSON response
    for salesman_id in assigned_jobs.keys():
        assert (
            salesman_id.isdigit()
        ), "Salesman ID should be a string in the JSON response"
        assert isinstance(
            assigned_jobs[salesman_id], list
        ), f"Jobs for salesman {salesman_id} should be a list"
        assert (
            len(assigned_jobs[salesman_id]) > 0
        ), f"Salesman {salesman_id} should have at least one assigned job"

    # ✅ Validate each job has required fields
    for salesman_id, job_list in assigned_jobs.items():
        for job in job_list:
            assert "job_id" in job, "Each job should contain 'job_id'"
            assert "date" in job, "Each job should contain 'date'"
            assert "location" in job, "Each job should contain 'location'"
            assert "duration_mins" in job, "Each job should contain 'duration_mins'"
            assert "entry_time" in job, "Each job should contain 'entry_time'"
            assert "exit_time" in job, "Each job should contain 'exit_time'"
            assert "salesman_id" in job, "Each job should contain 'salesman_id'"
            assert "start_time" in job, "Each job should contain 'start_time'"
