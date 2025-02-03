import pandas as pd
from app.models.schemas import ScheduleRequest

def generate_schedule(schedule_data: ScheduleRequest):
    # Convert the request data into Pandas DataFrames
    jobs_df = pd.DataFrame([job.model_dump() for job in schedule_data.jobs])
    cleaners_df = pd.DataFrame([cleaner.model_dump() for cleaner in schedule_data.cleaners])

    # Basic scheduling logic (to be replaced with heuristic clustering)
    jobs_df["assigned_cleaner"] = jobs_df.index % len(cleaners_df)  # Simple round-robin assignment

    return jobs_df.to_dict(orient="records")
