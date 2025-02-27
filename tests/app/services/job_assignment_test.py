from datetime import datetime
from app.models.job import Job
from app.models.salesman import Salesman
from app.models.location import Location
from app.services.job_assignment import assign_jobs


def test_assign_jobs():
    # Create Salesmen
    salesmen = [
        Salesman(
            salesman_id="1",
            home_location=Location(40.730610, -73.935242),
            start_time=datetime(2025, 2, 5, 9, 0, 0),
            end_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
        Salesman(
            salesman_id="2",
            home_location=Location(34.0522, -118.2437),
            start_time=datetime(2025, 2, 5, 9, 0, 0),
            end_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
        Salesman(
            salesman_id="3",
            home_location=Location(51.5074, -0.1278),
            start_time=datetime(2025, 2, 5, 9, 0, 0),
            end_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
    ]

    # Create Jobs
    jobs = [
        Job(
            job_id="1",
            date=datetime(2025, 2, 5),
            location=Location(40.730500, -73.935200),
            duration_mins=60,
            entry_time=datetime(2025, 2, 5, 10, 0, 0),
            exit_time=datetime(2025, 2, 5, 14, 0, 0),
        ),
        Job(
            job_id="2",
            date=datetime(2025, 2, 5),
            location=Location(34.0525, -118.2440),
            duration_mins=45,
            entry_time=datetime(2025, 2, 5, 11, 0, 0),
            exit_time=datetime(2025, 2, 5, 15, 0, 0),
        ),
        Job(
            job_id="3",
            date=datetime(2025, 2, 5),
            location=Location(51.5075, -0.1280),
            duration_mins=90,
            entry_time=datetime(2025, 2, 5, 12, 0, 0),
            exit_time=datetime(2025, 2, 5, 16, 0, 0),
        ),
    ]

    # Call assign_jobs function
    roster = assign_jobs(jobs, salesmen)

    # ✅ All jobs should be assigned
    assigned_salesmen = [
        job.salesman_id for job_list in roster.jobs.values() for job in job_list
    ]
    assert len(assigned_salesmen) == len(
        jobs
    ), "All jobs should be assigned to salesmen."

    # ✅ Each job should be assigned to the closest available salesman
    for job in jobs:
        assert (
            job.salesman_id is not None
        ), f"Job {job.job_id} should be assigned to a salesman."
        assert any(
            job in roster.jobs[sman.salesman_id] for sman in salesmen
        ), f"Job {job.job_id} should be in at least one salesman's job list."

    # ✅ Jobs should be assigned in chronological order
    for sman in salesmen:
        sman_jobs = roster.jobs.get(sman.salesman_id, [])
        for i in range(len(sman_jobs) - 1):
            assert (
                sman_jobs[i].entry_time <= sman_jobs[i + 1].entry_time
            ), f"Jobs for Salesman {sman.salesman_id} should be assigned in chronological order."
