from fastapi import FastAPI
from app.routes import scheduler

app = FastAPI(title="Travelling Salesman API")

# Include the scheduler API routes
app.include_router(scheduler.router)


@app.get("/")
def home():
    return {"message": "Travelling Salesman Backend Running"}
