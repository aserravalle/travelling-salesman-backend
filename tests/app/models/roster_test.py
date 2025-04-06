from datetime import date, datetime, timedelta
from app.models.roster_response import RosterResponse
from app.models.job import Job
from app.models.salesman import Salesman
from app.models.location import Location


def test_assign_first_job_to_salesman():
    sman = Salesman(
        salesman_id="1",
        location=Location(latitude=40.730610, longitude=-73.935242),
        start_time=datetime(2025, 2, 5, 9, 0, 0),
        end_time=datetime(2025, 2, 5, 17, 0, 0),
    )
    job = Job(
        job_id="1",
        date=datetime(2025, 2, 5),
        location=Location(latitude=40.7128, longitude=-74.0060),
        duration_mins=60,
        entry_time=datetime(2025, 2, 5, 10, 0, 0),
        exit_time=datetime(2025, 2, 5, 14, 0, 0),
    )
    roster = RosterResponse(roster_id="1", date=date(2025, 2, 5))
    roster.add_salesman(sman)

    job_start_time = datetime(2025, 2, 5, 10, 0, 0)
    roster.assign_job_to_salesman(job, sman, job_start_time)

    assert (
        job in roster.jobs[sman.salesman_id]
    ), "Job 1 should be added to the salesman's job list."
    assert job.salesman_id == sman.salesman_id, "Job 1 should be assigned to salesman 1"
    assert job.start_time == job_start_time, "Job 1 start time should be assigned"

    assert (
        sman.current_location == job.location
    ), "Salesman location should be updated to the most recent job location"
    assert sman.current_time == job_start_time + timedelta(
        minutes=job.duration_mins
    ), "Salesman time should be set to the jobs estimated completion time"
    assert (
        sman.start_time == job_start_time
    ), "Salesman's start time should be set on the first job."


def test_assign_multiple_jobs_to_salesman():
    sman = Salesman(
        salesman_id="2",
        location=Location(latitude=34.0522, longitude=-118.2437),
        start_time=datetime(2025, 2, 5, 9, 0, 0),
        end_time=datetime(2025, 2, 5, 17, 0, 0),
    )
    job1 = Job(
        job_id="1",
        date=datetime(2025, 2, 5),
        location=Location(latitude=34.0522, longitude=-118.2437),
        duration_mins=45,
        entry_time=datetime(2025, 2, 5, 10, 0, 0),
        exit_time=datetime(2025, 2, 5, 14, 0, 0),
    )
    job2 = Job(
        job_id="2",
        date=datetime(2025, 2, 5),
        location=Location(latitude=34.0000, longitude=-118.2500),
        duration_mins=30,
        entry_time=datetime(2025, 2, 5, 11, 0, 0),
        exit_time=datetime(2025, 2, 5, 15, 0, 0),
    )
    roster = RosterResponse(roster_id="1", date=date(2025, 2, 5))
    roster.add_salesman(sman)

    job1_start_time = datetime(2025, 2, 5, 10, 0, 0)
    roster.assign_job_to_salesman(job1, sman, job1_start_time)

    assert (
        sman.current_location == job1.location
    ), "Salesman location should be updated to first jobs location"
    assert sman.current_time == job1_start_time + timedelta(
        minutes=job1.duration_mins
    ), "Salesman current_time should be set to the first jobs completion time"

    job2_start_time = sman.current_time + timedelta(minutes=15)
    roster.assign_job_to_salesman(job2, sman, job2_start_time)

    assert (
        sman.current_location == job2.location
    ), "Salesman location should be updated to second jobs location"
    assert sman.current_time == job2_start_time + timedelta(
        minutes=job2.duration_mins
    ), "Salesman current_time should be updated to second jobs completion time"
    assert (
        job2 in roster.jobs[sman.salesman_id]
    ), "Job 2 should be added to the salesman's list"
