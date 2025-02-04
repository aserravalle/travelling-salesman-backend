from app.services.scheduler_logic import assign_jobs
from app.models.schemas import Job, Salesman
from datetime import datetime


def test_assign_jobs_logic():
    jobs = [
        Job(
            id=1,
            date=datetime(2025, 2, 5, 9, 0, 0),
            location=(10, 10),
            duration=60,
            entry_time=datetime(2025, 2, 5, 9, 0, 0),
            exit_time=datetime(2025, 2, 5, 12, 0, 0),
        ),
        Job(
            id=2,
            date=datetime(2025, 2, 5, 9, 0, 0),
            location=(20, 20),
            duration=60,
            entry_time=datetime(2025, 2, 5, 9, 0, 0),
            exit_time=datetime(2025, 2, 5, 12, 0, 0),
        ),
    ]

    salesmen = [
        Salesman(
            id=1,
            home_location=(40.730610, -73.935242),
            start_time=datetime(2025, 2, 5, 9, 0, 0),
            end_time=datetime(2025, 2, 5, 17, 0, 0),
        )
    ]

    result = assign_jobs(jobs, salesmen)

    assert isinstance(result, dict)
    assert 1 in result
    assert len(result[1]) > 0
