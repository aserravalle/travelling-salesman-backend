from datetime import datetime
from app.models.job import Job


def test_job_sorting():
    jobs = [
        Job(
            job_id="1",
            date=datetime(2025, 2, 6),
            location=(40.7128, -74.0060),
            duration_mins=60,
            entry_time=datetime(2025, 2, 6, 10, 0, 0),
            exit_time=datetime(2025, 2, 6, 14, 0, 0),
        ),
        Job(
            job_id="2",
            date=datetime(2025, 2, 6),
            location=(40.7128, -74.0060),
            duration_mins=60,
            entry_time=datetime(2025, 2, 6, 9, 30, 0),
            exit_time=datetime(2025, 2, 6, 14, 0, 0),
        ),
        Job(
            job_id="3",
            date=datetime(2025, 2, 6),
            location=(40.7128, -74.0060),
            duration_mins=60,
            entry_time=datetime(2025, 2, 6, 11, 0, 0),
            exit_time=datetime(2025, 2, 6, 14, 0, 0),
        ),
        Job(
            job_id="4",
            date=datetime(2025, 2, 6),
            location=(40.7128, -74.0060),
            duration_mins=60,
            entry_time=datetime(2025, 2, 6, 9, 30, 0),
            exit_time=datetime(2025, 2, 6, 11, 0, 0),
        ),
        Job(
            job_id="5",
            date=datetime(2025, 2, 6),
            location=(40.7128, -74.0060),
            duration_mins=30,
            entry_time=datetime(2025, 2, 6, 8, 0, 0),
            exit_time=datetime(2025, 2, 6, 8, 30, 0),
        ),
        Job(
            job_id="6",
            date=datetime(2025, 2, 6),
            location=(40.7128, -74.0060),
            duration_mins=90,
            entry_time=datetime(2025, 2, 6, 12, 0, 0),
            exit_time=datetime(2025, 2, 6, 13, 30, 0),
        ),
        Job(
            job_id="7",
            date=datetime(2025, 2, 6),
            location=(40.7128, -74.0060),
            duration_mins=45,
            entry_time=datetime(2025, 2, 6, 11, 0, 0),
            exit_time=datetime(2025, 2, 6, 11, 45, 0),
        ),
        Job(
            job_id="8",
            date=datetime(2025, 2, 6),
            location=(40.7128, -74.0060),
            duration_mins=120,
            entry_time=datetime(2025, 2, 6, 13, 0, 0),
            exit_time=datetime(2025, 2, 6, 15, 0, 0),
        ),
        Job(
            job_id="9",
            date=datetime(2025, 2, 6),
            location=(40.7128, -74.0060),
            duration_mins=15,
            entry_time=datetime(2025, 2, 6, 10, 0, 0),
            exit_time=datetime(2025, 2, 6, 10, 15, 0),
        ),
    ]

    jobs.sort(
        key=lambda job: (
            job.date,
            job.entry_time,
            job.duration_mins,
            job.exit_time - job.entry_time,
        )
    )

    expected_order = ["5", "4", "2", "9", "1", "7", "3", "6", "8"]
    sorted_ids = [job.job_id for job in jobs]

    assert (
        sorted_ids == expected_order
    ), f"Expected order {expected_order}, but got {sorted_ids}"
