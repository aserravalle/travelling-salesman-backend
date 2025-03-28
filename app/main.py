import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import scheduler
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Travelling Salesman API",
    description="API for generating job rosters using a dummy Traveling Salesman algorithm",
    version="1.0.1",
)

# allow_origins = os.getenv("ALLOW_ORIGINS", "http://localhost:8080").split(",")
allow_origins = ["*"]  # Allow all origins during development

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(scheduler.router)

@app.get("/")
def home():
    return {"message": "Travelling Salesman Backend Running"}