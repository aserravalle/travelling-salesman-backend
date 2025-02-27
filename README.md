# travelling-salesman-backend

Back end for the travelling salesman app, responsible for scheduling jobs.

## Running API

To set up and run the API locally, follow these steps:

1. Create a virtual environment:
    ```sh
    python -m venv venv
    ```

2. Activate the virtual environment:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Start the FastAPI server with Uvicorn:
    ```sh
    uvicorn app.main:app --reload
    ```

    This will start the server and enable hot-reloading, so any changes to the code will automatically restart the server. 

    After this, you can check API docs in http://127.0.0.1:8000/docs

## Running tests

To run all tests:

```sh
pytest tests/ -v
```

To run a specific test:

```sh
pytest tests/app/routes/test_scheduler_routes.py -v
```

## Project Structure

The project is organized as follows:

- `app/`: Contains the main application code.
  - `main.py`: The entry point of the FastAPI application.
  - `models/`: Contains the data models used in the application.
    - `job.py`: Defines the `Job` model.
    - `location.py`: Defines the `Location` model.
    - `roster.py`: Defines the `Roster` model.
    - `salesman.py`: Defines the `Salesman` model.
  - `routes/`: Contains the API route definitions.
    - `scheduler.py`: Defines the routes for job scheduling.
  - `services/`: Contains the business logic of the application.
    - `scheduler_logic.py`: Contains the logic for assigning jobs to salesmen.

- `tests/`: Contains the test cases for the application.
  - `app/`: Mirrors the structure of the `app/` directory for testing purposes.
    - `main.py`: Tests for the main application.
    - `models/`: Tests for the data models.
      - `job_test.py`: Tests for the `Job` model.
      - `location_test.py`: Tests for the `Location` model.
      - `roster_test.py`: Tests for the `Roster` model.
      - `salesman_test.py`: Tests for the `Salesman` model.
    - `routes/`: Tests for the API routes.
      - `scheduler_test.py`: Tests for the scheduler routes.
    - `services/`: Tests for the business logic.
      - `scheduler_logic_test.py`: Tests for the scheduler logic.

## Continuous Integration

The project uses GitHub Actions for continuous integration. The workflows are defined in the `.github/workflows/` directory:

- `testing.yml`: Runs the tests and checks the code formatting on each pull request.
- `formatting.yml`: Checks the code formatting with Black and linting with Flake8 on each pull request.

## Code Formatting and Linting

The project uses Black for code formatting and Flake8 for linting. The configuration for these tools is defined in the `setup.cfg` file.

To format the code with Black:

```sh
black .
```

To lint the code with Flake8:

```sh
flake8 .
```
