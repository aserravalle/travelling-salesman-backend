# Travelling Salesman API

A FastAPI-based service for optimizing job assignments using a simplified Travelling Salesman approach.

## Overview

This API provides functionality to assign jobs to salesmen efficiently, considering:
- Geographic locations
- Time windows
- Work duration constraints
- Travel times
- Maximum working hours

## Setup and Running

1. Create a virtual environment:
```sh
python -m venv venv
```

2. Activate the virtual environment:
```sh
# Windows
venv\Scripts\activate
```
# macOS/Linux
```sh
source venv/bin/activate
```

3. Install dependencies:
```sh
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

4. Start the server:
```sh
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## Development

### Running Tests
```sh
pytest tests/ -v
```

To run a specific test:

```sh
pytest tests/app/routes/test_scheduler_routes.py -v
```

### Linting
```sh
black .
flake8 .
```

## Continuous Integration

The project uses GitHub Actions for continuous integration. The workflows are defined in the `.github/workflows/` directory:

- `testing.yml`: Runs the tests and checks the code formatting on each pull request.
- `formatting.yml`: Checks the code formatting with Black and linting with Flake8 on each pull request.

## Project Structure

```
├── app/
│   ├── models/
│   │   ├── base_model.py     # Base Pydantic model configuration
│   │   ├── job.py           # Job data model
│   │   ├── location.py      # Location data model with distance calculations
│   │   ├── roster.py        # Roster data model for job assignments
│   │   └── salesman.py      # Salesman data model
│   ├── routes/
│   │   └── scheduler.py     # API endpoints for job scheduling
│   ├── services/
│   │   └── job_assignment.py # Core job assignment logic
│   └── main.py              # FastAPI application setup
├── tests/                    # Test suite
└── requirements.txt          # Project dependencies
```

## API Endpoints

### POST `/assign_jobs`
Assigns jobs to salesmen optimally.

#### Request Body
```json
{
  "jobs": [
    {
      "job_id": "string",
      "date": "datetime",
      "location": [float, float],
      "duration_mins": int,
      "entry_time": "datetime",
      "exit_time": "datetime"
    }
  ],
  "salesmen": [
    {
      "salesman_id": "string",
      "home_location": [float, float],
      "start_time": "datetime",
      "end_time": "datetime"
    }
  ]
}
```

#### Response
```json
{
  "jobs": {
    "salesman_id": [
      {
        "job_id": "string",
        "date": "datetime",
        "location": [float, float],
        "duration_mins": int,
        "entry_time": "datetime",
        "exit_time": "datetime",
        "salesman_id": "string",
        "start_time": "datetime"
      }
    ]
  },
  "unassigned_jobs": [],
  "message": "string"
}
```
