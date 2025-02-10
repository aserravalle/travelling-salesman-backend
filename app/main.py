from fastapi import FastAPI
from app.routes import scheduler

app = FastAPI(title="Travelling Salesman API")
app.include_router(scheduler.router)


@app.get("/")
def home():
    return {"message": "Travelling Salesman Backend Running"}
