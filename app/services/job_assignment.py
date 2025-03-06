from typing import List
from datetime import timedelta
from sklearn.cluster import KMeans
import numpy as np

from app.models.job import Job
from app.models.roster import RosterResponse
from app.models.salesman import Salesman


def assign_jobs(jobs: List[Job], salesmen: List[Salesman]) -> RosterResponse:
    """
    Assign jobs to salesmen optimally based on location and time constraints using K-Means clustering.

    The algorithm:
    1. Clusters jobs based on location using K-Means
    2. Assigns jobs to salesmen by cluster

    Args:
        jobs: List of jobs to assign
        salesmen: List of available salesmen

    Returns:
        Roster: Complete roster with job assignments and status
    """
    if not jobs:
        roster = RosterResponse()
        roster.add_salesmen(salesmen)
        roster.message = "No jobs to assign"
        return roster

    # Convert job locations to numpy array for clustering
    job_locations = np.array([[job.location[0], job.location[1]] for job in jobs])

    # Determine the number of clusters (e.g., number of salesmen)
    num_clusters = len(salesmen)

    # Perform K-Means clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(job_locations)
    job_clusters = kmeans.labels_

    # Create a roster response
    roster = RosterResponse()
    roster.add_salesmen(salesmen)

    # Assign jobs to salesmen by cluster
    for cluster_idx in range(num_clusters):
        cluster_jobs = [jobs[i] for i in range(len(jobs)) if job_clusters[i] == cluster_idx]
        if cluster_jobs:
            assign_jobs_to_salesman(cluster_jobs, salesmen[cluster_idx], roster)

    roster.message = _generate_roster_message(roster)
    return roster


def assign_jobs_to_salesman(jobs: List[Job], salesman: Salesman, roster: RosterResponse):
    """
    Assign jobs to a specific salesman based on availability and location.

    Args:
        jobs: List of jobs to assign
        salesman: Salesman to assign jobs to
        roster: Roster to update with job assignments
    """
    for job in sorted(jobs, key=lambda x: x.date):
        arrival_time = salesman.get_arrival_time(job)
        completion_time = arrival_time + timedelta(minutes=job.duration_mins)

        if salesman.can_complete_job_in_time(job.exit_time, completion_time):
            roster.assign_job_to_salesman(job, salesman, arrival_time)
        else:
            roster.unassigned_jobs.append(job)


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