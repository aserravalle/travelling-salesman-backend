import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import scheduler

app = FastAPI(
    title="Travelling Salesman API",
    description="API for generating job rosters using a dummy Traveling Salesman algorithm",
    version="1.0.1",
)
app.include_router(scheduler.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"], # TODO move this to env
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Travelling Salesman Backend Running"}
