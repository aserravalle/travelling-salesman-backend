from datetime import datetime
from app.models.location import Location
from app.models.salesman import Salesman


def test_can_complete_job_in_time():
    sman = Salesman(
        salesman_id="1",
        home_location=Location(40.730610, -73.935242),
        start_time=datetime(2025, 2, 5, 9, 0, 0),
        end_time=datetime(2025, 2, 5, 17, 0, 0),
    )

    assert sman.can_complete_job_in_time(
        job_exit_time=datetime(2025, 2, 5, 16, 0, 0),
        completion_time=datetime(2025, 2, 5, 15, 30, 0),
    ), "The salesman should be able to complete the job on time."

    assert sman.can_complete_job_in_time(
        job_exit_time=datetime(2025, 2, 5, 18, 0, 0),
        completion_time=datetime(2025, 2, 5, 17, 0, 0),
    ), "Should be able to complete job exactly at salesman end_time."

    assert sman.can_complete_job_in_time(
        job_exit_time=datetime(2025, 2, 5, 15, 0, 0),
        completion_time=datetime(2025, 2, 5, 15, 0, 0),
    ), "Should be able to complete job exactly at job exit_time."

    assert not sman.can_complete_job_in_time(
        job_exit_time=datetime(2025, 2, 5, 18, 0, 0),
        completion_time=datetime(2025, 2, 5, 17, 30, 0),
    ), "Should not be able to complete job due to salesman end_time."

    assert not sman.can_complete_job_in_time(
        job_exit_time=datetime(2025, 2, 5, 14, 30, 0),
        completion_time=datetime(2025, 2, 5, 15, 0, 0),
    ), "Should not be able to complete job due to job exit_time."

    assert not sman.can_complete_job_in_time(
        job_exit_time=datetime(2025, 2, 5, 18, 0, 0),
        completion_time=datetime(2025, 2, 5, 17, 1, 0),
    ), "Should not be able to complete job finishing 1 min past salesman end_time."

    assert not sman.can_complete_job_in_time(
        job_exit_time=datetime(2025, 2, 5, 15, 0, 0),
        completion_time=datetime(2025, 2, 5, 15, 1, 0),
    ), "Should not be able to complete job finishing 1 min past job exit_time."

    assert not sman.can_complete_job_in_time(
        job_exit_time=datetime(2025, 2, 5, 19, 0, 0),
        completion_time=datetime(2025, 2, 5, 17, 1, 0),  # 8h 1min since start_time
    ), "Should not be able to complete job exceeding max workday limit."
