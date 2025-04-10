from typing import List
from sklearn.cluster import KMeans
import numpy as np
from app.models.job import Job

def cluster_jobs(jobs: List[Job], n_clusters: int) -> None:
    """
    Clustering algorithm using KMeans to assign a cluster id to each job.
    Clusters are determined based on job locations (latitude and longitude).
    """
    job_locations = np.array([[job.location.latitude, job.location.longitude] for job in jobs])
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(job_locations)
    for job, cluster_id in zip(jobs, kmeans.labels_):
        job.cluster = int(cluster_id)
