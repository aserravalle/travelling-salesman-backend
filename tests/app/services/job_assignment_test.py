from datetime import datetime, timedelta
from app.models.job import Job
from app.models.salesman import Salesman
from app.models.location import Location
from app.services.job_assignment import assign_jobs
from unittest.mock import patch
from app.services.location_helpers import LocationHelpers


def test_assign_jobs():
    # Create Salesmen
    salesmen = [
        Salesman(
            salesman_id="1",
            location=Location(latitude=40.730610, longitude=-73.935242),
            start_time=datetime(2025, 2, 5, 9, 0, 0),
            end_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
        Salesman(
            salesman_id="2",
            location=Location(latitude=34.0522, longitude=-118.2437),
            start_time=datetime(2025, 2, 5, 9, 0, 0),
            end_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
        Salesman(
            salesman_id="3",
            location=Location(latitude=51.5074, longitude=-0.1278),
            start_time=datetime(2025, 2, 5, 9, 0, 0),
            end_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
    ]

    # Create Jobs
    jobs = [
        Job(
            job_id="1",
            date=datetime(2025, 2, 5),
            location=Location(latitude=40.730500, longitude=-73.935200),
            duration_mins=60,
            entry_time=datetime(2025, 2, 5, 10, 0, 0),
            exit_time=datetime(2025, 2, 5, 14, 0, 0),
        ),
        Job(
            job_id="2",
            date=datetime(2025, 2, 5),
            location=Location(latitude=34.0525, longitude=-118.2440),
            duration_mins=45,
            entry_time=datetime(2025, 2, 5, 11, 0, 0),
            exit_time=datetime(2025, 2, 5, 15, 0, 0),
        ),
        Job(
            job_id="3",
            date=datetime(2025, 2, 5),
            location=Location(latitude=51.5075, longitude=-0.1280),
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


def test_no_jobs_supplied():
    # Create Salesmen
    salesmen = [
        Salesman(
            salesman_id="1",
            location=Location(latitude=40.730610, longitude=-73.935242),
            start_time=datetime(2025, 2, 5, 9, 0, 0),
            end_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
        Salesman(
            salesman_id="2",
            location=Location(latitude=34.0522, longitude=-118.2437),
            start_time=datetime(2025, 2, 5, 9, 0, 0),
            end_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
    ]

    # Create empty job list
    jobs = []

    # Call assign_jobs function
    roster = assign_jobs(jobs, salesmen)

    # ✅ No jobs should be assigned
    assert len(roster.jobs["1"]) == 0, "No jobs should be assigned"
    assert len(roster.jobs["2"]) == 0, "No jobs should be assigned"
    assert len(roster.unassigned_jobs) == 0, "No jobs should be unassigned"

    # ✅ Validate message
    assert (
        roster.message == "No jobs to assign"
    ), "Message should indicate no jobs to assign"


def test_unassignable_jobs():
    # Create Salesmen
    salesmen = [
        Salesman(
            salesman_id="1",
            location=Location(latitude=40.730610, longitude=-73.935242),
            start_time=datetime(2025, 2, 5, 9, 0, 0),
            end_time=datetime(2025, 2, 5, 17, 0, 0),
        )
    ]

    # Create Jobs with one unassignable job
    jobs = [
        Job(
            job_id="1",
            date=datetime(2025, 2, 5),
            location=Location(latitude=40.730500, longitude=-73.935200),
            duration_mins=60,
            entry_time=datetime(2025, 2, 5, 10, 0, 0),
            exit_time=datetime(2025, 2, 5, 14, 0, 0),
        ),
        Job(
            job_id="2",
            date=datetime(2025, 2, 5),
            location=Location(latitude=34.0525, longitude=-118.2440),
            duration_mins=45,
            entry_time=datetime(2025, 2, 5, 11, 0, 0),
            exit_time=datetime(2025, 2, 5, 15, 0, 0),
        ),
        Job(
            job_id="3",
            date=datetime(2025, 2, 5),
            location=Location(latitude=51.5075, longitude=-0.1280),
            duration_mins=90,
            entry_time=datetime(
                2025, 2, 5, 18, 0, 0
            ),  # Unassignable job (outside working hours)
            exit_time=datetime(2025, 2, 5, 19, 0, 0),
        ),
    ]

    # Call assign_jobs function
    with patch.object(LocationHelpers, 'get_travel_time_minutes', return_value=20):
        roster = assign_jobs(jobs, salesmen)

    # ✅ Validate assigned jobs
    assert set(job.job_id for job in roster.jobs["1"]) == {
        "1",
        "2",
    }, "Salesman 1 should have job 1 and 2"

    # ✅ Validate unassigned jobs
    unassigned_jobs = roster.unassigned_jobs
    assert len(unassigned_jobs) == 1, "There should be an unassigned job"
    assert set(job.job_id for job in unassigned_jobs) == {
        "3",
    }, "The unassigned job should be 3"

    # ✅ Validate message
    assert (
        roster.message == "Roster completed with unassigned jobs"
    ), "Message should indicate unassigned jobs"


def test_assign_jobs_accounts_for_travel_time():
    # One salesman available 9-5
    salesman = Salesman(
        salesman_id="101",
        location=Location(latitude=34.0522, longitude=-118.2437),
        start_time=datetime(2025, 2, 5, 9, 0, 0),
        end_time=datetime(2025, 2, 5, 17, 0, 0),
    )

    jobs = [
        Job(
            job_id="1",
            date=datetime(2025, 2, 5),
            location=Location(latitude=34.0000, longitude=-118.2500),
            duration_mins=60,
            entry_time=datetime(2025, 2, 5, 9, 0, 0),
            exit_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
        Job(
            job_id="2",
            date=datetime(2025, 2, 5),
            location=Location(latitude=34.0522, longitude=-118.2437),
            duration_mins=45,
            entry_time=datetime(2025, 2, 5, 9, 1, 0),  # 1 minute after job 1
            exit_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
        Job(
            job_id="3",
            date=datetime(2025, 2, 5),
            location=Location(latitude=34.0000, longitude=-118.2500),
            duration_mins=90,
            entry_time=datetime(2025, 2, 5, 9, 2, 0),  # 1 minute after job 2
            exit_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
    ]

    with patch.object(LocationHelpers, 'get_travel_time_minutes', return_value=20):
        roster = assign_jobs(jobs, [salesman])

    start_times = [job.start_time for job in roster.jobs["101"]]
    assert len(start_times) == 3, "All jobs should be assigned"

    first_start_time = datetime(2025, 2, 5, 9, 0, 0)
    assert start_times[0] == first_start_time, "Job 1 should start at entry_time (9:00)"
    assert start_times[1] == start_times[0] + timedelta(minutes=60) + timedelta(minutes=20), "Job 2 should start later"
    assert start_times[2] == start_times[1] + timedelta(minutes=45) + timedelta(minutes=20), "Job 3 should start later"
    assert salesman.current_time == start_times[2] + timedelta(minutes=90), "Salesman should finish 1:30h later (90 duration)"
    assert salesman.time_worked_mins == 235, "Salesman should finish at 13:25"


def test_assign_jobs_accounts_for_travel_time_and_entry_time():
    # One salesman available 9-5
    salesman = Salesman(
        salesman_id="101",
        location=Location(latitude=34.0522, longitude=-118.2437),
        start_time=datetime(2025, 2, 5, 9, 0, 0),
        end_time=datetime(2025, 2, 5, 17, 0, 0),
    )

    jobs = [
        Job(
            job_id="1",
            date=datetime(2025, 2, 5),
            location=Location(latitude=34.0000, longitude=-118.2500),
            duration_mins=60,
            entry_time=datetime(
                2025, 2, 5, 9, 5, 0
            ),  # 5 minutes after salesman start time
            exit_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
        Job(
            job_id="2",
            date=datetime(2025, 2, 5),
            location=Location(latitude=34.0522, longitude=-118.2437),
            duration_mins=45,
            entry_time=datetime(2025, 2, 5, 9, 6, 0),  # 1 minute after job 1
            exit_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
        Job(
            job_id="3",
            date=datetime(2025, 2, 5),
            location=Location(latitude=34.0000, longitude=-118.2500),
            duration_mins=90,
            entry_time=datetime(2025, 2, 5, 9, 7, 0),  # 1 minute after job 2
            exit_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
    ]

    with patch.object(LocationHelpers, 'get_travel_time_minutes', return_value=20):
        roster = assign_jobs(jobs, [salesman])

    start_times = [job.start_time for job in roster.jobs["101"]]
    assert len(start_times) == 3, "3 jobs should be assigned"

    first_start_time = datetime(2025, 2, 5, 9, 5, 0)
    assert start_times[0] == first_start_time, "Job 1 should start at entry_time (9:05)"
    assert start_times[1] == start_times[0] + timedelta(minutes=60) + timedelta(minutes=20), "Job 2 should start 1:35h later (60 duration + 20 travel time)"
    assert start_times[2] == start_times[1] + timedelta(minutes=45) + timedelta(minutes=20), "Job 3 should start 1:20h later (45 duration + 20 travel time)"
    assert salesman.current_time == start_times[2] + timedelta(minutes=90), "Salesman should finish 1:30h later (90 duration)"
    assert salesman.time_worked_mins == 235, "Salesman should finish at 13:25"
