import json
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
from app.services.location_helpers import LocationHelpers

client = TestClient(app)


def test_assign_jobs_api():
    # Test job data
    request = {
        "jobs": [
            {
                "job_id": "1",
                "date": "2025-02-05 00:00:00",
                "location": { "latitude": 40.7128, "longitude": -74.0060 },
                "duration_mins": 60,
                "entry_time": "2025-02-05 09:00:00",
                "exit_time": "2025-02-05 12:00:00",
            },
            {
                "job_id": "2",
                "date": "2025-02-05 00:00:00",
                "location": { "latitude": 40.7130, "longitude": -74.0055 },
                "duration_mins": 45,
                "entry_time": "2025-02-05 09:30:00",
                "exit_time": "2025-02-05 14:00:00",
            },
            {
                "job_id": "3",
                "date": "2025-02-05 00:00:00",
                "location": { "address": "789 Pine Rd" },
                "duration_mins": 30,
                "entry_time": "2025-02-05 11:30:00",
                "exit_time": "2025-02-05 13:00:00",
            },
            {
                "job_id": "4",
                "date": "2025-02-05 00:00:00",
                "location": { "address": "2 Bass St" },
                "duration_mins": 90,
                "entry_time": "2025-02-05 12:30:00",
                "exit_time": "2025-02-05 15:00:00",
            }
        ],
        "salesmen": [
            {
                "salesman_id": "101",
                "location": { "latitude": 40.730610, "longitude": -73.935242 },
                "start_time": "2025-02-05 09:00:00",
                "end_time": "2025-02-05 17:00:00",
            },
            {
                "salesman_id": "102",
                "location": { "address": "102 Home" },
                "start_time": "2025-02-05 09:00:00",
                "end_time": "2025-02-05 17:00:00",
            }
        ]
    }

    # Send request to API
    with patch.object(LocationHelpers, 'get_travel_time_minutes', return_value=20):
        response = client.post("/assign_jobs", json=request)

    # ✅ Validate response status
    assert response.status_code == 200, "Response should have status 200"

    # ✅ Validate response structure
    response_json = response.json()
    assert isinstance(response_json, dict), "Response should be a dictionary"
    assert "jobs" in response_json, "Response should contain 'jobs'"
    assert (
        "unassigned_jobs" in response_json
    ), "Response should contain 'unassigned_jobs'"
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
    assert (
        response_json["message"] == "Roster completed with all jobs assigned"
    ), "Message should indicate all jobs are assigned"

    # ✅ Validate specific job assignments (replace with correct job_ids if needed)
    assert "101" in assigned_jobs, "Salesman 101 should have assigned jobs"
    assert "102" in assigned_jobs, "Salesman 102 should have assigned jobs"


def test_no_jobs_supplied():
    # Test data with no jobs
    request = {
        "jobs": [],
        "salesmen": [
            {
                "salesman_id": "101",
                "location": { "latitude": 40.730610, "longitude": -73.935242, "address": "101 Home" },
                "start_time": "2025-02-05 09:00:00",
                "end_time": "2025-02-05 17:00:00",
            },
            {
                "salesman_id": "102",
                "location": { "latitude": 40.750610, "longitude": -73.975242, "address": "102 Home" },
                "start_time": "2025-02-05 09:00:00",
                "end_time": "2025-02-05 17:00:00",
            },
        ],
    }

    # Send request to API
    with patch.object(LocationHelpers, 'get_travel_time_minutes', return_value=20):
        response = client.post("/assign_jobs", json=request)

    # ✅ Validate response status
    assert response.status_code == 200, "Response should have status 200"
    response_json = response.json()

    # ✅ Validate no jobs are assigned
    assert response_json["jobs"] == {
        "101": [],
        "102": [],
    }, "Salesmen should not have any jobs assigned"
    assert len(response_json["unassigned_jobs"]) == 0, "No jobs should be unassigned"

    # ✅ Validate message
    assert (
        response_json["message"] == "No jobs to assign"
    ), "Message should indicate no jobs to assign"


def test_unassignable_jobs():
    # Test job data with unassignable job
    request = {
        "jobs": [
            {
                "job_id": "1",
                "date": "2025-02-05 00:00:00",
                "location": { "latitude": 40.7128, "longitude": -74.0060, "address": "123 Main St" },
                "duration_mins": 60,
                "entry_time": "2025-02-05 09:00:00",
                "exit_time": "2025-02-05 12:00:00",
            },
            {
                "job_id": "2",
                "date": "2025-02-05 00:00:00",
                "location": { "latitude": 40.7130, "longitude": -74.0055, "address": "456 Oak Ave" },
                "duration_mins": 45,
                "entry_time": "2025-02-05 10:30:00",
                "exit_time": "2025-02-05 14:00:00",
            },
            {
                "job_id": "3",
                "date": "2025-02-05 00:00:00",
                "location": { "latitude": 40.7140, "longitude": -74.0050, "address": "789 Pine Rd" },
                "duration_mins": 30,
                "entry_time": "2025-02-05 18:30:00",
                "exit_time": "2025-02-05 19:00:00",
            },
        ],
        "salesmen": [
            {
                "salesman_id": "101",
                "location": { "latitude": 40.730610, "longitude": -73.935242, "address": "101 Home" },
                "start_time": "2025-02-05 09:00:00",
                "end_time": "2025-02-05 17:00:00",
            }
        ],
    }

    # Send request to API
    with patch.object(LocationHelpers, 'get_travel_time_minutes', return_value=20):
        response = client.post("/assign_jobs", json=request)

    # ✅ Validate response status
    assert response.status_code == 200, "Response should have status 200"
    response_json = response.json()

    # ✅ Validate assigned jobs
    assert set(job["job_id"] for job in response_json["jobs"]["101"]) == {
        "1",
        "2",
    }, "Salesman 101 should have jobs 1 and 2"

    # ✅ Validate unassigned jobs
    unassigned_jobs = response_json["unassigned_jobs"]
    assert isinstance(
        unassigned_jobs, list
    ), "Unassigned jobs should be returned as a list"
    assert len(unassigned_jobs) == 1, "There should be one unassigned job"
    assert (
        unassigned_jobs[0]["job_id"] == "3"
    ), "The unassigned job should be job_id '3'"

    # ✅ Validate message
    assert (
        response_json["message"] == "Roster completed with unassigned jobs"
    ), "Message should indicate unassigned jobs"


def test_assign_jobs_florence():
    with open("tests/app/routes/roster_request_florence.json", "r") as file:
        request = json.load(file)
    with patch.object(LocationHelpers, 'get_travel_time_minutes', return_value=20):
        response = client.post("/assign_jobs", json=request)
    assert response.status_code == 200, "Response should have status 200"

    response_json = response.json()
    expected = {
        "jobs": {
            "101": [
                {
                    "job_id": "1",
                    "client_name": "Airbnb 1",
                    "date": "2025-03-28T09:00:00",
                    "location": {
                        "latitude": 43.7677,
                        "longitude": 11.2593,
                        "address": "1 R, Via dei Neri, San Niccolò, Quartiere 1, Firenze, Toscana, 50122, Italia"
                    },
                    "duration_mins": 120,
                    "entry_time": "2025-03-28T08:00:00",
                    "exit_time": "2025-03-28T23:00:00",
                    "salesman_id": "101",
                    "salesman_name": "Francesco",
                    "start_time": "2025-03-28T09:00:00"
                },
                {
                    "job_id": "3",
                    "client_name": "Airbnb 3",
                    "date": "2025-03-28T09:00:00",
                    "location": {
                        "latitude": 43.7704,
                        "longitude": 11.2512,
                        "address": "Tornabuoni Beacci, 3, Via dei Tornabuoni, Oltrarno, Quartiere 1, Firenze, Toscana, 50123, Italia"
                    },
                    "duration_mins": 120,
                    "entry_time": "2025-03-28T11:00:00",
                    "exit_time": "2025-03-28T23:00:00",
                    "salesman_id": "101",
                    "salesman_name": "Francesco",
                    "start_time": "2025-03-28T11:20:00"
                }
            ],
            "102": [
                {
                    "job_id": "5",
                    "client_name": "Airbnb 5",
                    "date": "2025-03-28T09:00:00",
                    "location": {
                        "latitude": 43.7687,
                        "longitude": 11.2687,
                        "address": "5, Via Ghibellina, San Niccolò, Quartiere 1, Firenze, Toscana, 50121, Italia"
                    },
                    "duration_mins": 120,
                    "entry_time": "2025-03-28T08:40:00",
                    "exit_time": "2025-03-28T14:00:00",
                    "salesman_id": "102",
                    "salesman_name": "Alessio",
                    "start_time": "2025-03-28T09:00:00"
                },
                {
                    "job_id": "4",
                    "client_name": "Airbnb 4",
                    "date": "2025-03-28T09:00:00",
                    "location": {
                        "latitude": 43.7677,
                        "longitude": 11.2596,
                        "address": "4 R, Via dei Benci, San Niccolò, Quartiere 1, Firenze, Toscana, 50122, Italia"
                    },
                    "duration_mins": 120,
                    "entry_time": "2025-03-28T11:00:00",
                    "exit_time": "2025-03-28T23:00:00",
                    "salesman_id": "102",
                    "salesman_name": "Alessio",
                    "start_time": "2025-03-28T11:20:00"
                }
            ],
            "103": [
                {
                    "job_id": "7",
                    "client_name": "Airbnb 7",
                    "date": "2025-03-28T09:00:00",
                    "location": {
                        "latitude": 43.7689,
                        "longitude": 11.2606,
                        "address": "Piazza Santa Croce, San Niccolò, Quartiere 1, Firenze, Toscana, 50122, Italia"
                    },
                    "duration_mins": 120,
                    "entry_time": "2025-03-28T10:00:00",
                    "exit_time": "2025-03-28T14:30:00",
                    "salesman_id": "103",
                    "salesman_name": "Andrea",
                    "start_time": "2025-03-28T10:00:00"
                },
                {
                    "job_id": "2",
                    "client_name": "Airbnb 2",
                    "date": "2025-03-28T09:00:00",
                    "location": {
                        "latitude": 43.7714,
                        "longitude": 11.2507,
                        "address": "2, Via della Vigna Nuova, San Frediano, Quartiere 1, Firenze, Toscana, 50123, Italia"
                    },
                    "duration_mins": 90,
                    "entry_time": "2025-03-28T12:00:00",
                    "exit_time": "2025-03-28T23:00:00",
                    "salesman_id": "103",
                    "salesman_name": "Andrea",
                    "start_time": "2025-03-28T12:20:00"
                }
            ],
            "104": [
                {
                    "job_id": "6",
                    "client_name": "Airbnb 6",
                    "date": "2025-03-28T09:00:00",
                    "location": {
                        "latitude": 43.7738,
                        "longitude": 11.2547,
                        "address": "6, Borgo San Lorenzo, Quartiere 1, Firenze, Toscana, 50123, Italia"
                    },
                    "duration_mins": 120,
                    "entry_time": "2025-03-28T10:00:00",
                    "exit_time": "2025-03-28T23:00:00",
                    "salesman_id": "104",
                    "salesman_name": "Matteo",
                    "start_time": "2025-03-28T10:00:00"
                }
            ]
        },
        "unassigned_jobs": [],
        "message": "Roster completed with all jobs assigned"
    }

    # Assert that both have the same "unassigned_jobs" and "message"
    assert response_json["unassigned_jobs"] == expected["unassigned_jobs"], "Unassigned jobs should match"
    assert response_json["message"] == expected["message"], "Message should match"

    # Iterate through the "jobs" and ensure each is the same
    for salesman_id, jobs in expected["jobs"].items():
        assert salesman_id in response_json["jobs"], f"Salesman {salesman_id} should be in the response"
        for i in range(len(jobs)):
            expected_job = jobs[i]
            actual_job = response_json["jobs"][salesman_id][i]
            assert actual_job == expected_job, f"Expected the same assignment for {salesman_id} job index {i}"

# def test_invalid_address_does_not_break_api():
#     # Test data with no jobs
#     request = {
#         "jobs": [
#             {
#                 "job_id": "1",
#                 "date": "2025-02-05 00:00:00",
#                 "location": { "latitude": 40.7128, "longitude": -74.0060 },
#                 "duration_mins": 60,
#                 "entry_time": "2025-02-05 09:00:00",
#                 "exit_time": "2025-02-05 12:00:00",
#             },
#             {
#                 "job_id": "2",
#                 "date": "2025-02-05 00:00:00",
#                 "location": { "address": "invalid_address" },
#                 "duration_mins": 45,
#                 "entry_time": "2025-02-05 09:30:00",
#                 "exit_time": "2025-02-05 14:00:00",
#             }
#         ],
#         "salesmen": [
#             {
#                 "salesman_id": "101",
#                 "location": { "latitude": 40.730610, "longitude": -73.935242 },
#                 "start_time": "2025-02-05 09:00:00",
#                 "end_time": "2025-02-05 17:00:00",
#             }
#         ]
#     }

#     # Send request to API
#     response = client.post("/assign_jobs", json=request)

#     # ✅ Validate response status
#     assert response.status_code == 200, "Response should have status 200"
#     response_json = response.json()

#     # ✅ Validate no jobs are assigned
#     assert response_json["jobs"] == {
#         "101": [],
#         "102": [],
#     }, "Salesmen should not have any jobs assigned"
#     assert len(response_json["unassigned_jobs"]) == 0, "No jobs should be unassigned"

#     # ✅ Validate message
#     assert (
#         response_json["message"] == "No jobs to assign"
#     ), "Message should indicate no jobs to assign"
