from typing import List
from datetime import datetime, timedelta

from app.models.job import Job
from app.models.roster_daily import RosterResponse
from app.models.salesman import Salesman


def assign_jobs(jobs: List[Job], salesmen: List[Salesman]) -> RosterResponse:
    """
    Assign jobs to salesmen optimally based on location and time constraints.

    The algorithm:
    1. Sorts jobs by date and time
    2. For each job, finds the best available salesman based on:
       - Travel time to job location
       - Available working hours
       - Maximum working day constraints

    Args:
        jobs: List of jobs to assign
        salesmen: List of available salesmen

    Returns:
        Roster: Complete roster with job assignments and status
    """
    jobs = sorted(jobs)
    roster = RosterResponse()
    roster.add_salesmen(salesmen)

    if not jobs:
        roster.message = "No jobs to assign"
        return roster

    for job in jobs:
        best_assignment = _find_best_salesman(job, salesmen)

        if best_assignment:
            salesman, start_time = best_assignment
            roster.assign_job_to_salesman(job, salesman, start_time)
        else:
            roster.unassigned_jobs.append(job)

    roster.message = _generate_roster_message(roster)
    return roster


def _find_best_salesman(
    job: Job, salesmen: List[Salesman]
) -> tuple[Salesman, datetime] | None:
    """
    Find the best salesman for a job based on availability and location.

    Args:
        job: Job to assign
        salesmen: List of available salesmen

    Returns:
        tuple: (best_salesman, start_time) or None if no suitable salesman found
    """
    best_salesman = None
    best_time = None

    for salesman in salesmen:
        arrival_time = salesman.get_arrival_time(job)
        completion_time = arrival_time + timedelta(minutes=job.duration_mins)

        if not salesman.can_complete_job_in_time(job.exit_time, completion_time):
            continue

        if best_salesman is None or arrival_time < best_time:
            best_salesman = salesman
            best_time = arrival_time

    return (best_salesman, best_time) if best_salesman else None


def _generate_roster_message(roster: RosterResponse) -> str:
    """
    Generate an appropriate status message for the roster.

    Args:
        roster: The completed roster

    Returns:
        str: Status message
    """
    if not any(roster.jobs.values()):
        return "No jobs to assign"
    elif roster.unassigned_jobs:
        return "Roster completed with unassigned jobs"
    return "Roster completed with all jobs assigned"
