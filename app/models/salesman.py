from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional

from app.models.job import Job
from app.models.location import Location


class Salesman(BaseModel):
    salesman_id: str
    home_location: Location                         # starting location of the salesman
    start_time: datetime                            # earliest available start datetime of the salesman
    end_time: datetime                              # latest available end datetime of the salesman
    current_location: Optional[Location] = None     # current location of the salesman during job assignment
    current_time: Optional[datetime] = None         # current datetime of the salesman during job assignment
    time_worked_mins: Optional[int] = 0             # how long the salesman has already worked today
    max_workday_mins: Optional[int] = 8 * 60  # maximum workday is 8h

    def can_complete_job_in_time(self, job_exit_time, completion_time) -> bool:
        job_finished_in_time = completion_time <= min(self.end_time, job_exit_time)
        salesman_exceeds_max_hours = (completion_time - self.start_time) > timedelta(minutes=self.max_workday_mins)
        return job_finished_in_time and not salesman_exceeds_max_hours

    def assign_to_salesman(self, job: Job) -> None:
        if self.is_first_job():
            self.start_time = job.start_time
        self.current_location = job.location
        self.current_time = job.start_time + timedelta(minutes=job.duration_mins)

    def is_first_job(self):
        return self.current_time == self.start_time

    def get_arrival_time(self, job: Job) -> datetime:
        travel_time = self.current_location.travel_time_to(job.location)
        return max(self.current_time + travel_time, job.entry_time)
