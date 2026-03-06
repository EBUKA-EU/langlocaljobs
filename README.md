# LangLocalJobs Backend

This is the backend for the LangLocalJobs project, built with Flask and SQLAlchemy.

## Project Structure

```
langlocaljobs/
│   README.md
│   requirements.txt
│   .flake8
│   pyproject.toml
│   .editorconfig
│
└───backend/
    │   run.py
    │
    └───app/
        │   __init__.py
        │   config.py
        │   extension.py
        │
        ├───models/
        │   __init__.py
        ├───routes/
        │   __init__.py
        ├───services/
        │   __init__.py
        └───utils/
    ├───migrations/
    └───tests/
```

## Setup Instructions

1. **Clone the repository**

    ```sh
    git clone <repo-url>
    cd langlocaljobs
    ```

2. **Create and activate a virtual environment**

    ```sh
    python -m venv .venv
    # On Windows:
    .venv\Scripts\activate
    # On macOS/Linux:
    source .venv/bin/activate
    ```

3. **Install dependencies**

    ```sh
    pip install -r requirements.txt
    ```

4. **Run the backend server**

    ```sh
    cd backend
    python run.py
    ```

    The server will start at http://127.0.0.1:5000

5. **Check the health endpoint**
   Visit [http://127.0.0.1:5000/api/health](http://127.0.0.1:5000/api/health) to verify the backend is running.

## Linting and Formatting

- **Lint:**
    ```sh
    flake8
    ```
- **Format:**
    ```sh
    black .
    ```

## Key Files and Folders

- `backend/run.py`: Main entrypoint to start the Flask server.
- `backend/app/__init__.py`: App factory and route registration.
- `backend/app/config.py`: Configuration settings for Flask and database.
- `backend/app/extension.py`: Database and migration extension setup.
- `backend/app/models/`: Place for SQLAlchemy models.
- `backend/app/routes/`: Place for API route handlers.
- `backend/app/services/`: Place for business logic/services.
- `backend/app/utils/`: Place for utility/helper functions.
- `backend/migrations/`: Database migration scripts (auto-managed).
- `backend/tests/`: Unit and integration tests.
- `requirements.txt`: Python dependencies.
- `.flake8`, `pyproject.toml`, `.editorconfig`: Linting, formatting, and editor settings.

---

For further development, I will add models, routes, and services in the respective folders as well as new features.
