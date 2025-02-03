from app.services.scheduler_logic import generate_schedule
from app.models.schemas import ScheduleRequest, Job, Cleaner

def test_generate_schedule():
    schedule_data = ScheduleRequest(
        jobs=[
            Job(property_id=1, duration=90, time_window="ENTRADA"),
            Job(property_id=2, duration=60, time_window="SALIDA")
        ],
        cleaners=[
            Cleaner(cleaner_id=101, name="John", hours_available=8, home_address="Valencia"),
            Cleaner(cleaner_id=102, name="Jane", hours_available=8, home_address="Valencia")
        ]
    )

    schedule_result = generate_schedule(schedule_data)

    assert isinstance(schedule_result, list)
    assert len(schedule_result) == 2
    assert "property_id" in schedule_result[0]
    assert "assigned_cleaner" in schedule_result[0]
