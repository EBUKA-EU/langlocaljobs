# LangLocalJobs

LangLocalJobs is a full-stack web application that aggregates language-related job listings through web scraping and presents them in a searchable, user-friendly interface. Users can browse jobs, save listings, and track applications, while admins can manage the platform.

---

## Table of Contents

- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Local Setup](#local-setup)
    - [Prerequisites](#prerequisites)
    - [Backend Setup](#backend-setup)
    - [Frontend Setup](#frontend-setup)
    - [Environment Variables](#environment-variables)
    - [Database Migrations](#database-migrations)
- [User Guide](#user-guide)
    - [Registration & Login](#registration--login)
    - [Browsing Jobs](#browsing-jobs)
    - [Saving & Applying to Jobs](#saving--applying-to-jobs)
    - [User Dashboard](#user-dashboard)
    - [Admin Dashboard](#admin-dashboard)
- [API Reference](#api-reference)
    - [Authentication](#authentication-endpoints)
    - [Jobs](#jobs-endpoints)
    - [Users](#users-endpoints)
    - [Recruiters](#recruiters-endpoints)
- [Linting & Formatting](#linting--formatting)
- [Running Tests](#running-tests)

---

## Tech Stack

| Layer      | Technology                                                     |
| ---------- | -------------------------------------------------------------- |
| Frontend   | React 19, React Router v7, Axios, TanStack Query, Tailwind CSS |
| Backend    | Python 3, Flask 3, Flask-SQLAlchemy, Flask-Migrate, Flask-CORS |
| Database   | SQLite (development) / PostgreSQL (production)                 |
| Auth       | JWT (PyJWT), Werkzeug password hashing                         |
| Scraping   | Requests, BeautifulSoup4                                       |
| Migrations | Alembic via Flask-Migrate                                      |

---

## Project Structure

```
langlocaljobs/
├── README.md
├── requirements.txt
├── pyproject.toml
│
├── backend/
│   ├── run.py                  # App entry point
│   └── app/
│       ├── __init__.py         # App factory
│       ├── config.py           # Configuration classes
│       ├── extension.py        # Flask extensions (db, migrate)
│       ├── models/             # SQLAlchemy models
│       ├── routes/             # API blueprints
│       │   ├── auth.py         # /api/auth/*
│       │   ├── jobs.py         # /api/jobs/*
│       │   ├── users.py        # /api/users/*
│       │   └── recruiters.py   # /api/recruiters/*
│       ├── services/
│       │   └── scraping.py     # Job scraping logic
│       └── utils/
│
├── frontend/
│   ├── public/
│   └── src/
│       ├── api/                # Axios API client modules
│       ├── components/         # Reusable UI components
│       └── pages/              # Route-level page components
│
└── migrations/                 # Alembic migration scripts
```

---

## Local Setup

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** and **npm**
- **Git**

### Backend Setup

1. **Clone the repository**

    ```sh
    git clone https://github.com/EBUKA-EU/langlocaljobs.git
    cd langlocaljobs
    ```

2. **Create and activate a virtual environment**

    ```sh
    python -m venv .venv

    # Windows
    .venv\Scripts\activate

    # macOS / Linux
    source .venv/bin/activate
    ```

3. **Install Python dependencies**

    ```sh
    pip install -r requirements.txt
    ```

4. **Create a `.env` file** in the project root (see [Environment Variables](#environment-variables))

5. **Apply database migrations**

    ```sh
    flask --app backend/app db upgrade
    ```

6. **Start the backend server**

    ```sh
    cd backend
    python run.py
    ```

    The API will be available at `http://127.0.0.1:5000`.

### Frontend Setup

1. **Navigate to the frontend directory**

    ```sh
    cd frontend
    ```

2. **Install dependencies**

    ```sh
    npm install
    ```

3. **Start the development server**

    ```sh
    npm start
    ```

    The app will open at `http://localhost:3000`.

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///langlocaljobs.db
FLASK_ENV=development
```

| Variable       | Description                                           | Default                      |
| -------------- | ----------------------------------------------------- | ---------------------------- |
| `SECRET_KEY`   | Secret used to sign JWT tokens — must be kept private | Required                     |
| `DATABASE_URL` | SQLAlchemy database connection string                 | `sqlite:///langlocaljobs.db` |
| `FLASK_ENV`    | Set to `production` for production deployments        | `development`                |

> **Never commit `.env` to source control.** A `.env.example` file should be used as a template.

### Database Migrations

The project uses Alembic via Flask-Migrate.

```sh
# Apply all pending migrations
flask --app backend/app db upgrade

# Create a new migration after changing models
flask --app backend/app db migrate -m "describe the change"

# Roll back the last migration
flask --app backend/app db downgrade
```

---

## User Guide

### Registration & Login

1. Navigate to `http://localhost:3000/register`.
2. Fill in your **name**, **email address**, and **password**, then click **Register**.
3. Once registered, go to `/login` and sign in with your credentials.
4. A JWT token is issued on login and stored in the browser. It expires after **24 hours**.

### Browsing Jobs

- After logging in, the **Jobs** page (`/jobs`) shows a paginated list of scraped job listings.
- Use the **search bar** to filter by job title keyword.
- Use the filter controls to narrow results by **location**, **company**, or **date range**.
- Click any job card to view full details on the **Job Details** page.

### Saving & Applying to Jobs

- On any job listing, click **Save** to bookmark it for later. Saved jobs appear in your dashboard.
- Click **Mark as Applied** to track jobs you have applied to externally. The application date is recorded automatically.
- To remove a saved job, click **Unsave** from the saved jobs list.

### User Dashboard

- Visit `/dashboard` to see:
    - Your **saved jobs** list
    - Your **applied jobs** list with timestamps
    - Your profile information (name, email, role)

### Admin Dashboard

Admin users have access to `/admin` which provides:

- A list of **all registered users** with the ability to update roles or delete accounts.
- A list of **all applied jobs** across every user.
- The ability to **edit or delete** any job listing.
- A list of **recruiters** registered on the platform.

> To grant admin access, update a user's `role` to `"admin"` directly in the database, or use the `PATCH /api/users/<id>` endpoint with an existing admin account.

---

## API Reference

Base URL (local): `http://127.0.0.1:5000`

All protected endpoints require a JWT token in the `Authorization` header:

```
Authorization: Bearer <token>
```

---

### Authentication Endpoints

#### `POST /api/auth/register`

Register a new user account.

**Request body:**

```json
{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "password": "securepassword"
}
```

**Response `201`:**

```json
{
    "message": "registration successful",
    "user": {
        "id": 1,
        "email": "jane@example.com",
        "name": "Jane Smith",
        "created_at": "2026-04-09T10:00:00Z",
        "role": "user"
    }
}
```

---

#### `POST /api/auth/login`

Log in and receive a JWT token.

**Request body:**

```json
{
    "email": "jane@example.com",
    "password": "securepassword"
}
```

**Response `200`:**

```json
{
    "message": "login successful",
    "user": {
        "id": 1,
        "email": "jane@example.com",
        "name": "Jane Smith",
        "role": "user",
        "last_logged_in": "2026-04-09T10:05:00Z"
    },
    "token": "<jwt_token>"
}
```

---

#### `POST /api/auth/logout`

Stateless logout. The frontend should discard the stored token.

**Response `200`:**

```json
{ "message": "logout successful" }
```

---

### Jobs Endpoints

All jobs endpoints require authentication (`Authorization: Bearer <token>`).

#### `GET /api/jobs`

List jobs with optional filtering and pagination.

**Query parameters:**

| Parameter   | Type   | Description                             |
| ----------- | ------ | --------------------------------------- |
| `page`      | int    | Page number (default: `1`)              |
| `per_page`  | int    | Results per page (default: `10`)        |
| `search`    | string | Filter by job title keyword             |
| `location`  | string | Filter by location                      |
| `company`   | string | Filter by company name                  |
| `date_from` | string | Filter jobs posted on/after (ISO date)  |
| `date_to`   | string | Filter jobs posted on/before (ISO date) |

**Response `200`:**

```json
{
    "jobs": [
        {
            "id": 1,
            "title": "Language Instructor",
            "company": "Acme Corp",
            "location": "London, UK",
            "url": "https://example.com/job/1",
            "posted_at": "2026-04-01T09:00:00"
        }
    ],
    "total": 42,
    "page": 1,
    "per_page": 10,
    "pages": 5,
    "has_next": true,
    "has_prev": false
}
```

---

#### `GET /api/jobs/<job_id>`

Get full details for a single job.

**Response `200`:**

```json
{
    "id": 1,
    "title": "Language Instructor",
    "company": "Acme Corp",
    "location": "London, UK",
    "description": "Full job description here...",
    "url": "https://example.com/job/1",
    "posted_at": "2026-04-01T09:00:00"
}
```

---

#### `PATCH /api/jobs/<job_id>` _(Admin only)_

Update a job listing. Updatable fields: `title`, `company`, `location`, `description`, `url`, `recruiter_id`.

**Response `200`:** `{ "message": "Job 1 updated successfully." }`

---

#### `DELETE /api/jobs/<job_id>` _(Admin only)_

Delete a job listing.

**Response `200`:** `{ "message": "Job 1 deleted successfully." }`

---

#### `GET /api/jobs/saved`

List the authenticated user's saved jobs.

**Response `200`:**

```json
{
    "saved_jobs": [
        {
            "id": 1,
            "title": "...",
            "company": "...",
            "location": "...",
            "url": "...",
            "saved_at": "..."
        }
    ]
}
```

---

#### `POST /api/jobs/<job_id>/save`

Save a job. Returns `201` on success, `200` if already saved.

---

#### `DELETE /api/jobs/<job_id>/save`

Remove a job from the saved list.

---

#### `GET /api/jobs/applied`

List the authenticated user's applied jobs.

---

#### `POST /api/jobs/<job_id>/apply`

Mark a job as applied.

**Response `201`:** `{ "message": "Marked as applied", "applied_at": "2026-04-09T10:10:00" }`

---

#### `GET /api/admin/applied-jobs` _(Admin only)_

List all job applications across all users.

---

### Users Endpoints

#### `GET /api/users/me`

Get the authenticated user's own profile.

**Response `200`:**

```json
{
    "id": 1,
    "email": "jane@example.com",
    "name": "Jane Smith",
    "role": "user",
    "created_at": "2026-04-09T10:00:00"
}
```

---

#### `PATCH /api/users/<user_id>`

Update a user. Users may only update their own record. Admins may update any user, including changing `role`.

**Request body (any combination of):**

```json
{
    "name": "Jane Doe",
    "password": "newpassword",
    "role": "admin"
}
```

**Response `200`:** `{ "message": "User 1 updated successfully." }`

---

#### `GET /api/users` _(Admin only)_

List all users.

---

#### `GET /api/users/<user_id>` _(Admin only)_

Get a user by ID.

---

#### `DELETE /api/users/<user_id>` _(Admin only)_

Delete a user by ID.

---

### Recruiters Endpoints

#### `POST /api/recruiters`

Create a recruiter profile for an existing user.

**Request body:**

```json
{
    "user_id": 1,
    "company_name": "Acme Languages Ltd",
    "website": "https://acme.example.com"
}
```

**Response `201`:** Returns the new recruiter object.

---

#### `GET /api/recruiters` _(Admin only)_

List all recruiter profiles.

---

#### `GET /api/recruiters/<recruiter_id>` _(Admin only)_

Get a recruiter profile by ID.

---

#### `PATCH /api/recruiters/<recruiter_id>`

Update a recruiter profile. Recruiters may only update their own profile. Admins may update any.

Updatable fields: `company_name`, `website`.

---

## Linting & Formatting

```sh
# Check code style
flake8

# Auto-format code
black .
```

---

## Running Tests

```sh
cd backend
pytest tests/
```
