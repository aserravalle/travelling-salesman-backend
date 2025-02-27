from fastapi import FastAPI
from app.routes import scheduler

app = FastAPI(
    title="Travelling Salesman API",
    description="API for generating job rosters using a dummy Traveling Salesman algorithm",
    version="1.0.1",
)
app.include_router(scheduler.router)


@app.get("/")
def home():
    return {"message": "Travelling Salesman Backend Running"}
