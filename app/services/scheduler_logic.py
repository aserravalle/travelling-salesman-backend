from datetime import timedelta
from typing import List

from app.models.job import Job
from app.models.roster import Roster
from app.models.salesman import Salesman


def assign_jobs(jobs: List[Job], salesmen: List[Salesman]) -> Roster:
    jobs = sorted(jobs)
    roster = Roster(
        roster_id="1",
        date=jobs[0].date,
    )
    roster.add_salesmen(salesmen)

    for job in jobs:
        best_salesman = None
        best_time = None

        for sman in salesmen:
            arrival_time = sman.get_arrival_time(job)
            completion_time = arrival_time + timedelta(minutes=job.duration_mins)

            if not sman.can_complete_job_in_time(job.exit_time, completion_time):
                continue

            if best_salesman is None or arrival_time < best_time:
                best_salesman = sman
                best_time = arrival_time

        if best_salesman:
            roster.assign_job_to_salesman(job, best_salesman, best_time)
        else:
            raise ValueError(
                f"Job {job.job_id} cannot be assigned due to time constraints."
            )  # TODO error handling

    return roster
