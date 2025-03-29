from datetime import datetime, timedelta
from app.models.job import Job
from app.models.salesman import Salesman
from app.models.location import Location
from app.services.job_assignment import assign_jobs


def test_assign_jobs():
    # Create Salesmen
    salesmen = [
        Salesman(
            salesman_id="1",
            location=Location(latitude=40.730610, longitude=-73.935242),
            start_time=datetime(2025, 2, 5, 9, 0, 0),
            end_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
        Salesman(
            salesman_id="2",
            location=Location(latitude=34.0522, longitude=-118.2437),
            start_time=datetime(2025, 2, 5, 9, 0, 0),
            end_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
        Salesman(
            salesman_id="3",
            location=Location(latitude=51.5074, longitude=-0.1278),
            start_time=datetime(2025, 2, 5, 9, 0, 0),
            end_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
    ]

    # Create Jobs
    jobs = [
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

    # Call assign_jobs function
    roster = assign_jobs(jobs, salesmen)

    # ✅ All jobs should be assigned
    assigned_salesmen = [
        job.salesman_id for job_list in roster.jobs.values() for job in job_list
    ]
    assert len(assigned_salesmen) == len(
        jobs
    ), "All jobs should be assigned to salesmen."

    # ✅ Each job should be assigned to the closest available salesman
    for job in jobs:
        assert (
            job.salesman_id is not None
        ), f"Job {job.job_id} should be assigned to a salesman."
        assert any(
            job in roster.jobs[sman.salesman_id] for sman in salesmen
        ), f"Job {job.job_id} should be in at least one salesman's job list."

    # ✅ Jobs should be assigned in chronological order
    for sman in salesmen:
        sman_jobs = roster.jobs.get(sman.salesman_id, [])
        for i in range(len(sman_jobs) - 1):
            assert (
                sman_jobs[i].entry_time <= sman_jobs[i + 1].entry_time
            ), f"Jobs for Salesman {sman.salesman_id} should be assigned in chronological order."


def test_no_jobs_supplied():
    # Create Salesmen
    salesmen = [
        Salesman(
            salesman_id="1",
            location=Location(latitude=40.730610, longitude=-73.935242),
            start_time=datetime(2025, 2, 5, 9, 0, 0),
            end_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
        Salesman(
            salesman_id="2",
            location=Location(latitude=34.0522, longitude=-118.2437),
            start_time=datetime(2025, 2, 5, 9, 0, 0),
            end_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
    ]

    # Create empty job list
    jobs = []

    # Call assign_jobs function
    roster = assign_jobs(jobs, salesmen)

    # ✅ No jobs should be assigned
    assert len(roster.jobs["1"]) == 0, "No jobs should be assigned"
    assert len(roster.jobs["2"]) == 0, "No jobs should be assigned"
    assert len(roster.unassigned_jobs) == 0, "No jobs should be unassigned"

    # ✅ Validate message
    assert (
        roster.message == "No jobs to assign"
    ), "Message should indicate no jobs to assign"


def test_unassignable_jobs():
    # Create Salesmen
    salesmen = [
        Salesman(
            salesman_id="1",
            location=Location(latitude=40.730610, longitude=-73.935242),
            start_time=datetime(2025, 2, 5, 9, 0, 0),
            end_time=datetime(2025, 2, 5, 17, 0, 0),
        )
    ]

    # Create Jobs with one unassignable job
    jobs = [
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
            entry_time=datetime(
                2025, 2, 5, 18, 0, 0
            ),  # Unassignable job (outside working hours)
            exit_time=datetime(2025, 2, 5, 19, 0, 0),
        ),
    ]

    # Call assign_jobs function
    roster = assign_jobs(jobs, salesmen)

    # ✅ Validate assigned jobs
    assert set(job.job_id for job in roster.jobs["1"]) == {
        "1",
        "2",
    }, "Salesman 1 should have job 1 and 2"

    # ✅ Validate unassigned jobs
    unassigned_jobs = roster.unassigned_jobs
    assert len(unassigned_jobs) == 1, "There should be an unassigned job"
    assert set(job.job_id for job in unassigned_jobs) == {
        "3",
    }, "The unassigned job should be 3"

    # ✅ Validate message
    assert (
        roster.message == "Roster completed with unassigned jobs"
    ), "Message should indicate unassigned jobs"


def test_assign_jobs_accounts_for_travel_time():
    # One salesman available 9-5
    salesman = Salesman(
        salesman_id="101",
        location=Location(latitude=34.0522, longitude=-118.2437),
        start_time=datetime(2025, 2, 5, 9, 0, 0),
        end_time=datetime(2025, 2, 5, 17, 0, 0),
    )

    jobs = [
        Job(
            job_id="1",
            date=datetime(2025, 2, 5),
            location=Location(latitude=34.0000, longitude=-118.2500),
            duration_mins=60,
            entry_time=datetime(2025, 2, 5, 9, 0, 0),
            exit_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
        Job(
            job_id="2",
            date=datetime(2025, 2, 5),
            location=Location(latitude=34.0522, longitude=-118.2437),
            duration_mins=45,
            entry_time=datetime(2025, 2, 5, 9, 1, 0),  # 1 minute after job 1
            exit_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
        Job(
            job_id="3",
            date=datetime(2025, 2, 5),
            location=Location(latitude=34.0000, longitude=-118.2500),
            duration_mins=90,
            entry_time=datetime(2025, 2, 5, 9, 2, 0),  # 1 minute after job 2
            exit_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
    ]

    roster = assign_jobs(jobs, [salesman])

    start_times = [job.start_time for job in roster.jobs["101"]]
    assert len(start_times) == 3, "All jobs should be assigned"

    first_start_time = datetime(2025, 2, 5, 9, 0, 0)
    assert start_times[0] == first_start_time, "Job 1 should start at entry_time (9:00)"
    assert start_times[1] == start_times[0] + timedelta(minutes=60) + timedelta(minutes=20), "Job 2 should start later"
    assert start_times[2] == start_times[1] + timedelta(minutes=45) + timedelta(minutes=20), "Job 3 should start later"
    assert salesman.current_time == start_times[2] + timedelta(minutes=90), "Salesman should finish 1:30h later (90 duration)"
    assert salesman.time_worked_mins == 235, "Salesman should finish at 13:25"


def test_assign_jobs_accounts_for_travel_time_and_entry_time():
    # One salesman available 9-5
    salesman = Salesman(
        salesman_id="101",
        location=Location(latitude=34.0522, longitude=-118.2437),
        start_time=datetime(2025, 2, 5, 9, 0, 0),
        end_time=datetime(2025, 2, 5, 17, 0, 0),
    )

    jobs = [
        Job(
            job_id="1",
            date=datetime(2025, 2, 5),
            location=Location(latitude=34.0000, longitude=-118.2500),
            duration_mins=60,
            entry_time=datetime(
                2025, 2, 5, 9, 5, 0
            ),  # 5 minutes after salesman start time
            exit_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
        Job(
            job_id="2",
            date=datetime(2025, 2, 5),
            location=Location(latitude=34.0522, longitude=-118.2437),
            duration_mins=45,
            entry_time=datetime(2025, 2, 5, 9, 6, 0),  # 1 minute after job 1
            exit_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
        Job(
            job_id="3",
            date=datetime(2025, 2, 5),
            location=Location(latitude=34.0000, longitude=-118.2500),
            duration_mins=90,
            entry_time=datetime(2025, 2, 5, 9, 7, 0),  # 1 minute after job 2
            exit_time=datetime(2025, 2, 5, 17, 0, 0),
        ),
    ]

    roster = assign_jobs(jobs, [salesman])

    start_times = [job.start_time for job in roster.jobs["101"]]
    assert len(start_times) == 3, "3 jobs should be assigned"

    first_start_time = datetime(2025, 2, 5, 9, 5, 0)
    assert start_times[0] == first_start_time, "Job 1 should start at entry_time (9:05)"
    assert start_times[1] == start_times[0] + timedelta(minutes=60) + timedelta(minutes=20), "Job 2 should start 1:35h later (60 duration + 20 travel time)"
    assert start_times[2] == start_times[1] + timedelta(minutes=45) + timedelta(minutes=20), "Job 3 should start 1:20h later (45 duration + 20 travel time)"
    assert salesman.current_time == start_times[2] + timedelta(minutes=90), "Salesman should finish 1:30h later (90 duration)"
    assert salesman.time_worked_mins == 235, "Salesman should finish at 13:25"


def test_assign_jobs_stress_test():

    with open("tests/data/salesman_test_data.csv", "r") as f:
        salesmen_lines = f.readlines()

    salesmen = []
    for line in salesmen_lines[1:]:  # Skip header
        fields = line.strip().split(",")
        salesmen.append(
            Salesman(
                salesman_id=fields[0],
                location=Location(latitude=float(fields[1]), longitude=float(fields[2])),
                start_time=datetime.strptime(fields[3], "%d-%m-%Y %H:%M"),
                end_time=datetime.strptime(fields[4], "%d-%m-%Y %H:%M"),
            )
        )

    with open("tests/data/jobs_test_data.csv", "r") as f:
        jobs_lines = f.readlines()

    jobs = []
    for line in jobs_lines[1:]:  # Skip header
        fields = line.strip().split(",")
        jobs.append(
            Job(
                job_id=fields[0],
                date=datetime.strptime(fields[1], "%d-%m-%Y %H:%M"),
                location=Location(latitude=float(fields[2]), longitude=float(fields[3])),
                duration_mins=int(fields[4]),
                entry_time=datetime.strptime(fields[5], "%d-%m-%Y %H:%M"),
                exit_time=datetime.strptime(fields[6], "%d-%m-%Y %H:%M"),
            )
        )

    # Call assign_jobs function
    roster = assign_jobs(jobs, salesmen)
    assert len(roster.jobs) > 0, "Jobs should be assigned"

    # Format roster.jobs as CSV string
    csv_lines = ["salesman_id,job_id,start_time"]
    for salesman_id, assigned_jobs in roster.jobs.items():
        for job in assigned_jobs:
            csv_lines.append(
                f"{salesman_id},\t{job.job_id},\t{job.start_time.strftime('%Y-%m-%d %H:%M:%S')}"
            )

    for job in roster.unassigned_jobs:
        csv_lines.append(f"NA ,\t{job.job_id}")

    actual = "\n".join(csv_lines)

    expected = """salesman_id,job_id,start_time
101,	7,	2025-02-05 09:00:00
101,	35,	2025-02-05 10:05:00
101,	22,	2025-02-05 12:25:00
101,	48,	2025-02-05 14:45:00
102,	32,	2025-02-05 09:00:00
102,	36,	2025-02-05 10:05:00
102,	10,	2025-02-05 11:10:00
102,	45,	2025-02-05 13:30:00
102,	49,	2025-02-05 14:50:00
103,	1,	2025-02-05 09:00:00
103,	20,	2025-02-05 10:50:00
103,	11,	2025-02-05 12:10:00
103,	43,	2025-02-05 13:15:00
103,	27,	2025-02-05 15:35:00
104,	28,	2025-02-05 09:05:00
104,	9,	2025-02-05 10:25:00
104,	41,	2025-02-05 12:15:00
104,	24,	2025-02-05 13:35:00
104,	16,	2025-02-05 14:55:00
105,	33,	2025-02-05 09:15:00
105,	30,	2025-02-05 10:35:00
105,	23,	2025-02-05 12:55:00
105,	25,	2025-02-05 14:00:00
106,	18,	2025-02-05 09:15:00
106,	39,	2025-02-05 11:35:00
106,	14,	2025-02-05 13:55:00
107,	8,	2025-02-05 09:30:00
107,	37,	2025-02-05 10:50:00
107,	40,	2025-02-05 12:10:00
107,	44,	2025-02-05 13:15:00
107,	47,	2025-02-05 14:20:00
108,	34,	2025-02-05 09:30:00
108,	31,	2025-02-05 11:20:00
108,	12,	2025-02-05 12:25:00
108,	46,	2025-02-05 13:45:00
108,	4,	2025-02-05 15:35:00
109,	29,	2025-02-05 09:35:00
109,	21,	2025-02-05 11:25:00
109,	13,	2025-02-05 13:15:00
109,	50,	2025-02-05 15:05:00
110,	19,	2025-02-05 09:45:00
110,	38,	2025-02-05 10:50:00
110,	42,	2025-02-05 12:40:00
110,	15,	2025-02-05 14:30:00
110,	5,	2025-02-05 15:35:00
NA ,	26
NA ,	51
NA ,	17
NA ,	2
NA ,	3
NA ,	6"""

    assert actual == expected, f"Expected:\n{expected}\n\nActual:\n{actual}"
