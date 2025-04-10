from datetime import datetime
import unittest
from unittest.mock import MagicMock
from app.services.clustering_service import cluster_jobs
from app.models.job import Job
from app.models.location import Location

class TestClusteringService(unittest.TestCase):
    def setUp(self):
        # Create mock jobs with mock locations
        self.jobs = [
            Job(
                job_id="1",
                date=datetime(2025, 2, 5),
                location=Location(latitude=40.730500, longitude=-73.935200),
                duration_mins=60,
                entry_time=datetime(2025, 2, 5, 10, 0, 0),
                exit_time=datetime(2025, 2, 5, 14, 0, 0),
            ),
            Job(
                job_id="2",
                date=datetime(2025, 2, 5),
                location=Location(latitude=34.0525, longitude=-118.2440),
                duration_mins=45,
                entry_time=datetime(2025, 2, 5, 11, 0, 0),
                exit_time=datetime(2025, 2, 5, 15, 0, 0),
            ),
            Job(
                job_id="3",
                date=datetime(2025, 2, 5),
                location=Location(latitude=51.5075, longitude=-0.1280),
                duration_mins=90,
                entry_time=datetime(2025, 2, 5, 12, 0, 0),
                exit_time=datetime(2025, 2, 5, 16, 0, 0),
            ),
        ]

    def test_cluster_jobs(self):
        # Call the clustering function
        cluster_jobs(self.jobs, n_clusters=2)

        # Assert that each job has been assigned a cluster
        cluster_ids = [job.cluster for job in self.jobs]
        self.assertEqual(len(set(cluster_ids)), 2)  # Ensure 2 clusters are created
        for job in self.jobs:
            self.assertIsInstance(job.cluster, int)  # Ensure cluster IDs are integers

if __name__ == "__main__":
    unittest.main()
