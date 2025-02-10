from app.models.schemas import Job, Salesman
from datetime import timedelta
from typing import List, Dict, Tuple


def assign_jobs(jobs: List[Job], salesmen: List[Salesman]) -> Dict[int, List[int]]:
    jobs = prioritise_jobs(jobs)
    roster = {s.salesman_id: [] for s in salesmen}
    salesmen_status = {
        s.salesman_id: {"location": s.home_location, "time": s.start_time}
        for s in salesmen
    }

    for job in jobs:
        best_salesman = None
        best_time = None

        for salesman in salesmen:
            state = salesmen_status[salesman.salesman_id]
            travel_time = calculate_travel_time(
                from_location=state["time"], to_location=job.location
            )

            # for each salesman, check the time the job would be completed after travel
            arrival_time = state["time"] + travel_time
            if arrival_time < job.entry_time:
                arrival_time = job.entry_time
            completion_time = arrival_time + timedelta(minutes=job.duration)

            # if the completion is outside availability hours for the job or salesman, they cannot complete the job
            if completion_time > min(salesman.end_time, job.exit_time):
                continue

            # if the completion is 8h after the salesman starts, they cannot complete the job
            if completion_time - salesman.start_time > timedelta(hours=8):
                continue

            if best_salesman is None or arrival_time < best_time:
                best_salesman = salesman
                best_time = arrival_time

        if best_salesman:
            roster[best_salesman.salesman_id].append(job.job_id)
            salesmen_status[best_salesman.salesman_id]["location"] = job.location
            salesmen_status[best_salesman.salesman_id]["time"] = best_time + timedelta(
                minutes=job.duration
            )
        else:
            print("job cannot be assigned")

    return roster

def prioritise_jobs(jobs: List[Job]):
    jobs_copy = jobs.copy()
    jobs_copy.sort(key=lambda x: (x.date, x.entry_time, x.exit_time - x.entry_time))
    return jobs_copy


def calculate_travel_time(
    from_location: Tuple[float, float], to_location: Tuple[float, float]
):
    # TODO euclidian distance algorithm for determining rough distance between these points.
    return timedelta(minutes=30)
