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
    os.getenv("ALLOW_ORIGINS", "").strip('"').split(","),  # Get production URL from .env and remove quotes
]

# Filter out empty strings from origins
origins = [origin for origin in origins if origin]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
)

app.include_router(scheduler.router)

@app.get("/")
def home():
    return {"message": "Travelling Salesman Backend Running"}