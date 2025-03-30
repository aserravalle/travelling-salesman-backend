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

# Configure CORS
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

# Add production URLs from environment variable
env_origins = os.getenv("ALLOW_ORIGINS", "").strip('"').split(",")
origins.extend(env_origins)

# Filter out empty strings from origins
origins = [origin.strip() for origin in origins if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scheduler.router)

@app.get("/")
def home():
    return {"message": "Travelling Salesman Backend Running"}