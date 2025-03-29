from datetime import datetime
from app.models.location import Location
from app.models.salesman import Salesman


def test_can_complete_job_in_time():
    sman = Salesman(
        salesman_id="1",
        location=Location(latitude=40.730610, longitude=-73.935242),
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


def test_salesman_sorting():
    salesmen = [
        Salesman(
            salesman_id="101",
            location=Location(latitude=0, longitude=0),
            start_time=datetime(2025, 2, 5, 10, 0, 0),  # second start time
            end_time=datetime(2025, 2, 5, 17, 0, 0),
            current_time=datetime(2025, 2, 5, 9, 0, 0),  # first current time
        ),
        Salesman(
            salesman_id="102",
            location=Location(latitude=0, longitude=0),
            start_time=datetime(2025, 2, 5, 9, 0, 0),  # first start time
            end_time=datetime(2025, 2, 5, 17, 0, 0),
            current_time=datetime(2025, 2, 5, 10, 0, 0),  # second current time
        ),
        Salesman(
            salesman_id="103",
            location=Location(latitude=0, longitude=0),
            start_time=datetime(2025, 2, 5, 10, 0, 0),  # second start time
            end_time=datetime(2025, 2, 5, 17, 0, 0),
            current_time=datetime(2025, 2, 5, 10, 0, 0),  # second current time
        ),
        Salesman(
            salesman_id="104",
            location=Location(latitude=0, longitude=0),
            start_time=datetime(2025, 2, 5, 10, 0, 0),  # second start time
            end_time=datetime(2025, 2, 5, 17, 0, 0),
            # null current time
        ),
        Salesman(
            salesman_id="105",
            location=Location(latitude=0, longitude=0),
            start_time=datetime(2025, 2, 5, 10, 0, 0),  # second start time
            end_time=datetime(2025, 2, 5, 17, 0, 0),
            current_time=datetime(2025, 2, 5, 11, 0, 0),  # third current time
        ),
        Salesman(
            salesman_id="106",
            location=Location(latitude=0, longitude=0),
            start_time=datetime(2025, 2, 5, 11, 0, 0),  # third start time
            end_time=datetime(2025, 2, 5, 17, 0, 0),
            # null current time
        ),
        Salesman(
            salesman_id="107",
            location=Location(latitude=0, longitude=0),
            start_time=datetime(2025, 2, 5, 9, 0, 0),  # first start time
            end_time=datetime(2025, 2, 5, 17, 0, 0),
            # null current time
        ),
    ]

    salesmen.sort()
    expected_order = ["101", "107", "102", "103", "104", "105", "106"]
    sorted_ids = [job.salesman_id for job in salesmen]

    assert (
        sorted_ids == expected_order
    ), f"Expected order {expected_order}, but got {sorted_ids}"
