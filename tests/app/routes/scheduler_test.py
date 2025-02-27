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
            {
                "job_id": "3",
                "date": "2025-02-05T11:00:00",
                "location": [40.7140, -74.0050],
                "duration_mins": 30,
                "entry_time": "2025-02-05T11:30:00",
                "exit_time": "2025-02-05T13:00:00",
            },
            {
                "job_id": "4",
                "date": "2025-02-05T12:00:00",
                "location": [40.7150, -74.0045],
                "duration_mins": 90,
                "entry_time": "2025-02-05T12:30:00",
                "exit_time": "2025-02-05T15:00:00",
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
    assert "unassigned_jobs" in response_json, "Response should contain 'unassigned_jobs'"
    assert "message" in response_json, "Response should contain 'message'"

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

    # ✅ Validate message
    assert response_json["message"] == "Roster completed with all jobs assigned", "Message should indicate all jobs are assigned"

    # ✅ Validate specific job assignments (replace with correct job_ids if needed)
    assert "101" in assigned_jobs, "Salesman 101 should have assigned jobs"
    assert "102" in assigned_jobs, "Salesman 102 should have assigned jobs"
    assert set(job["job_id"] for job in assigned_jobs["101"]) == {"1", "3"}, "Salesman 101 should have jobs 1 and 3"
    assert set(job["job_id"] for job in assigned_jobs["102"]) == {"2", "4"}, "Salesman 102 should have jobs 2 and 4"

def test_no_jobs_supplied():
    # Test data with no jobs
    request = {
        "jobs": [],
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
    assert "unassigned_jobs" in response_json, "Response should contain 'unassigned_jobs'"
    assert "message" in response_json, "Response should contain 'message'"

    # ✅ Validate no jobs are assigned
    assert len(response_json["jobs"]) == 0, "No jobs should be assigned"
    assert len(response_json["unassigned_jobs"]) == 0, "No jobs should be unassigned"

    # ✅ Validate message
    assert response_json["message"] == "No jobs to assign", "Message should indicate no jobs to assign"

def test_unassignable_jobs():
    # Test job data with unassignable job
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
            {
                "job_id": "3",
                "date": "2025-02-05T18:00:00",  # Unassignable job (outside working hours)
                "location": [40.7140, -74.0050],
                "duration_mins": 30,
                "entry_time": "2025-02-05T18:30:00",
                "exit_time": "2025-02-05T19:00:00",
            },
        ],
        "salesmen": [
            {
                "salesman_id": "101",
                "home_location": [40.730610, -73.935242],
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
    assert "unassigned_jobs" in response_json, "Response should contain 'unassigned_jobs'"
    assert "message" in response_json, "Response should contain 'message'"

    # ✅ Validate assigned jobs
    assert set(job["job_id"] for job in response_json["jobs"]["101"]) == {"1", "2"}, "Salesman 101 should have jobs 1 and 2"

    # ✅ Validate unassigned jobs
    unassigned_jobs = response_json["unassigned_jobs"]
    assert isinstance(unassigned_jobs, list), "Unassigned jobs should be returned as a list"
    assert len(unassigned_jobs) == 1, "There should be one unassigned job"
    assert unassigned_jobs[0]["job_id"] == "3", "The unassigned job should be job_id '3'"

    # ✅ Validate message
    assert response_json["message"] == "Roster completed with unassigned jobs", "Message should indicate unassigned jobs"
