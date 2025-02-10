from datetime import datetime
from app.models.job import Job  # Ensure this matches your module structure


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
        ),  # Earlier entry
        Job(
            job_id="3",
            date=datetime(2025, 2, 5),
            location=(40.7128, -74.0060),
            duration_mins=60,
            entry_time=datetime(2025, 2, 5, 11, 0, 0),
            exit_time=datetime(2025, 2, 5, 14, 0, 0),
        ),  # Earlier date
        Job(
            job_id="4",
            date=datetime(2025, 2, 6),
            location=(40.7128, -74.0060),
            duration_mins=60,
            entry_time=datetime(2025, 2, 6, 9, 30, 0),
            exit_time=datetime(2025, 2, 6, 11, 0, 0),
        ),  # Shorter window
    ]

    # Sort jobs in place
    jobs.sort()

    # Expected order:
    # 1. Job 3 (earliest date)
    # 2. Job 4 (same date as others but earliest entry time and shortest window)
    # 3. Job 2 (earlier entry time)
    # 4. Job 1 (latest entry time)

    expected_order = ["3", "4", "2", "1"]  # IDs in the expected sorted order
    sorted_ids = [job.job_id for job in jobs]

    assert (
        sorted_ids == expected_order
    ), f"Expected order {expected_order}, but got {sorted_ids}"
