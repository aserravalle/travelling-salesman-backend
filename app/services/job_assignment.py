from typing import List
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
import numpy as np

from app.models.job import Job
from app.models.roster_response import RosterResponse
from app.models.salesman import Salesman


def cluster_jobs(jobs: List[Job], n_clusters: int) -> None:
    """
    Clustering algorithm using KMeans to assign a cluster id to each job.
    Clusters are determined based on job locations (latitude and longitude).
    """
    job_locations = np.array([[job.location.latitude, job.location.longitude] for job in jobs])
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(job_locations)
    for job, cluster_id in zip(jobs, kmeans.labels_):
        job.cluster = int(cluster_id)


def assign_jobs(jobs: List[Job], salesmen: List[Salesman]) -> RosterResponse:
    """
    Optimally assign jobs to salesmen based on urgency, clusters, and time constraints.
    
    The flow is:
    1. Sort jobs by urgency.
    2. Cluster jobs into 4 clusters.
    3. Copy jobs and salesmen into unassigned/ unrostered lists.
    4. For each salesman (one at a time) assign jobs until they reach capacity:
         a. Look over unassigned jobs (skipping jobs whose clusters are in exhausted_clusters)
            to find the first job the salesman can complete.
         b. Once found, focus on that job’s cluster:
             i. Iterate over jobs in that cluster (ordered by urgency) and assign all that the salesman can complete.
            ii. Remove each assigned job from the working list and, if no more jobs in this cluster can be assigned, mark the cluster as exhausted.
         c. If no assignable job is found outside exhausted clusters, the salesman is considered at capacity.
         d. Remove all jobs assigned in this iteration from unassigned jobs.
    5. After all salesmen are processed (or no more assignable jobs exist),
       any remaining jobs are left as unassigned in the final roster.
    """
    cluster_jobs(jobs, n_clusters=4)

    roster = RosterResponse()
    roster.add_salesmen(salesmen)

    if not jobs:
        roster.message = "No jobs to assign"
        return roster

    unassigned_jobs = sorted(jobs, reverse=True)
    unrostered_salesmen = salesmen.copy()

    # Process one salesman at a time.
    while unassigned_jobs and unrostered_salesmen:
        # Get the next salesman to work
        salesman = unrostered_salesmen.pop(0)
        exhausted_clusters = set()  # Clusters that this salesman cannot accept any more jobs from
        print("Assigning jobs to:", salesman.salesman_id)

        # Continue assigning jobs until salesman is at capacity.
        while not salesman.is_at_capacity():
            ############################################################################
            ## Step 1: Try assign first job of iteration from non-exhausted clusters. ##
            ############################################################################
            first_job = None
            for job in unassigned_jobs:
                if job.cluster in exhausted_clusters:
                    continue
                arrival_time = _get_arrival_time_if_possible(salesman, job)
                if job_starts_after_salesman(roster, salesman, job):
                    arrival_time = None
                if arrival_time is not None:
                    # Assign the first job from a non-exhausted cluster.
                    roster.assign_job_to_salesman(job, salesman, arrival_time)
                    unassigned_jobs.remove(job)
                    first_job = job
                    break
            if first_job is None:
                # No assignable job found for remaining non-exhausted clusters.
                salesman.wait(15)
                continue

            #############################################################
            ## Step 2: Try to assign subsequent jobs from same cluster ##
            #############################################################

            current_cluster = first_job.cluster
            clustered_unassigned_jobs = [job for job in unassigned_jobs if job.cluster == current_cluster]

            # Iterate to assign as many jobs from this cluster as possible.
            while not salesman.is_at_capacity() and clustered_unassigned_jobs:
                job_assigned_in_cluster = False
                # We iterate over clustered_jobs (which is assumed to be ordered by urgency)
                for job in clustered_unassigned_jobs.copy():
                    arrival_time = _get_arrival_time_if_possible(salesman, job)
                    if arrival_time is not None:
                        roster.assign_job_to_salesman(job, salesman, arrival_time)
                        unassigned_jobs.remove(job)
                        clustered_unassigned_jobs.remove(job)
                        job_assigned_in_cluster = True
                        break # Once a job is assigned, restart the loop over clustered_jobs.
                # If no job in the current cluster could be assigned, mark this cluster exhausted.
                if not job_assigned_in_cluster:
                    exhausted_clusters.add(current_cluster)
                    break  # Exit the clustered_jobs loop and try to find a job from a different cluster.

            #################################################################
            ## Step 3: If the salesman is still not at capacity, try again ##
            #################################################################

    # Whatever jobs remain are unassigned.
    roster.unassigned_jobs.extend(unassigned_jobs)
    roster.message = _generate_roster_message(roster)
    return roster

def job_starts_after_salesman(roster, salesman, job):
    """
    First job should be assigned to the salesman at the start of their workday.
    """
    return len(roster.jobs[salesman.salesman_id]) == 0 and job.entry_time > salesman.current_time


def _get_arrival_time_if_possible(salesman: Salesman, job: Job) -> datetime | None:
    """
    Check if the salesman can start and complete the job given time and location constraints.
    Args:
        salesman: Salesman to check.
        job: Job to evaluate.
    Returns:
        Calculated arrival time if possible; otherwise None.
    """
    travel_time = salesman.current_location.travel_time_to(job.location)
    arrival_time = salesman.get_arrival_time(job, travel_time)
    completion_time = arrival_time + timedelta(minutes=job.duration_mins)

    if not salesman.can_complete_job_in_time(job.exit_time, completion_time):
        return None

    return arrival_time


def _generate_roster_message(roster: RosterResponse) -> str:
    """
    Generate a status message for the roster.
    """
    if not any(roster.jobs.values()):
        return "No jobs to assign"
    elif roster.unassigned_jobs:
        return "Roster completed with unassigned jobs"
    return "Roster completed with all jobs assigned"
