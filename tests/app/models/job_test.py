from datetime import datetime
from app.models.job import Job
from app.models.location import Location
import pytest


def test_job_creation():
    # Test basic job creation
    location = Location(latitude=40.7128, longitude=-74.0060)
    job = Job(
        job_id="1",
        date=datetime(2025, 2, 6),
        location=location,
        duration_mins=60,
        entry_time=datetime(2025, 2, 6, 10, 0, 0),
        exit_time=datetime(2025, 2, 6, 14, 0, 0),
    )
    assert job.job_id == "1"
    assert job.location == location
    assert job.duration_mins == 60
    assert job.salesman_id is None
    assert job.start_time is None
    assert job._travel_time_mins == 0

    # Test job creation with client name
    job = Job(
        job_id="2",
        client_name="Test Client",
        date=datetime(2025, 2, 6),
        location=location,
        duration_mins=60,
        entry_time=datetime(2025, 2, 6, 10, 0, 0),
        exit_time=datetime(2025, 2, 6, 14, 0, 0),
    )
    assert job.client_name == "Test Client"


def test_job_assign_salesman():
    location = Location(latitude=40.7128, longitude=-74.0060)
    job = Job(
        job_id="1",
        date=datetime(2025, 2, 6),
        location=location,
        duration_mins=60,
        entry_time=datetime(2025, 2, 6, 10, 0, 0),
        exit_time=datetime(2025, 2, 6, 14, 0, 0),
    )
    
    start_time = datetime(2025, 2, 6, 11, 0, 0)
    job.assign_salesman("S1", start_time)
    
    assert job.salesman_id == "S1"
    assert job.start_time == start_time


def test_job_sorting():
    location = Location(latitude=40.7128, longitude=-74.0060)
    jobs = [
        Job(
            job_id="1",
            date=datetime(2025, 2, 6),
            location=location,
            duration_mins=60,
            entry_time=datetime(2025, 2, 6, 10, 0, 0),
            exit_time=datetime(2025, 2, 6, 14, 0, 0),
        ),
        Job(
            job_id="2",
            date=datetime(2025, 2, 6),
            location=location,
            duration_mins=60,
            entry_time=datetime(2025, 2, 6, 9, 30, 0),
            exit_time=datetime(2025, 2, 6, 14, 0, 0),
        ),
        Job(
            job_id="3",
            date=datetime(2025, 2, 6),
            location=location,
            duration_mins=60,
            entry_time=datetime(2025, 2, 6, 11, 0, 0),
            exit_time=datetime(2025, 2, 6, 14, 0, 0),
        ),
        Job(
            job_id="4",
            date=datetime(2025, 2, 6),
            location=location,
            duration_mins=60,
            entry_time=datetime(2025, 2, 6, 9, 30, 0),
            exit_time=datetime(2025, 2, 6, 11, 0, 0),
        ),
        Job(
            job_id="5",
            date=datetime(2025, 2, 6),
            location=location,
            duration_mins=30,
            entry_time=datetime(2025, 2, 6, 8, 0, 0),
            exit_time=datetime(2025, 2, 6, 8, 30, 0),
        ),
        Job(
            job_id="6",
            date=datetime(2025, 2, 6),
            location=location,
            duration_mins=90,
            entry_time=datetime(2025, 2, 6, 12, 0, 0),
            exit_time=datetime(2025, 2, 6, 13, 30, 0),
        ),
        Job(
            job_id="7",
            date=datetime(2025, 2, 6),
            location=location,
            duration_mins=45,
            entry_time=datetime(2025, 2, 6, 11, 0, 0),
            exit_time=datetime(2025, 2, 6, 11, 45, 0),
        ),
        Job(
            job_id="8",
            date=datetime(2025, 2, 6),
            location=location,
            duration_mins=120,
            entry_time=datetime(2025, 2, 6, 13, 0, 0),
            exit_time=datetime(2025, 2, 6, 15, 0, 0),
        ),
        Job(
            job_id="9",
            date=datetime(2025, 2, 6),
            location=location,
            duration_mins=15,
            entry_time=datetime(2025, 2, 6, 10, 0, 0),
            exit_time=datetime(2025, 2, 6, 10, 15, 0),
        ),
    ]

    jobs.sort()

    expected_order = ["5", "4", "2", "9", "1", "7", "3", "6", "8"]
    sorted_ids = [job.job_id for job in jobs]

    assert sorted_ids == expected_order, f"Expected order {expected_order}, but got {sorted_ids}"


def test_job_validation():
    location = Location(latitude=40.7128, longitude=-74.0060)
    
    # Test invalid duration
    with pytest.raises(ValueError):
        Job(
            job_id="1",
            date=datetime(2025, 2, 6),
            location=location,
            duration_mins=0,  # Must be greater than 0
            entry_time=datetime(2025, 2, 6, 10, 0, 0),
            exit_time=datetime(2025, 2, 6, 14, 0, 0),
        )

    # Test exit time before entry time
    with pytest.raises(ValueError):
        Job(
            job_id="1",
            date=datetime(2025, 2, 6),
            location=location,
            duration_mins=60,
            entry_time=datetime(2025, 2, 6, 14, 0, 0),
            exit_time=datetime(2025, 2, 6, 10, 0, 0),
        )
