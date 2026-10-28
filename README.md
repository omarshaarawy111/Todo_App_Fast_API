# Todo App FastAPI

A server-rendered todo application built with FastAPI, SQLAlchemy, SQLite, Jinja2, and Bootstrap.

## Features

- User registration and authentication with JWT tokens
- Password hashing with Passlib and bcrypt
- Create, view, update, and delete todo items
- Role-based administrative routes
- HTML templates rendered with Jinja2
- Database migrations managed with Alembic
- Automated tests with pytest

## Project structure

```text
Todo_App_Fast_API/
├── alembic/       Database migration environment and revisions
├── routers/       Authentication, user, todo, and admin routes
├── static/        CSS and JavaScript assets
├── templates/     Jinja2 HTML templates
├── test/          Application tests and test database helpers
├── database.py    SQLAlchemy engine and session configuration
├── main.py        FastAPI application entry point
├── models.py      SQLAlchemy ORM models
└── requirements.txt
```

## Setup

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run the application

From the directory that contains `Todo_App_Fast_API`, run:

```powershell
uvicorn Todo_App_Fast_API.main:app --reload
```

Open [Todo App](https://todo-app-fast-api.onrender.com) in a browser.

## Database migrations

Apply the existing Alembic migrations with:

```powershell
alembic upgrade head
```

Create a new migration after changing the models with:

```powershell
alembic revision --autogenerate -m "Describe the schema change"
```

## Run tests

```powershell
python -m pytest
```

Local SQLite database files are created automatically when the application or test suite runs. They are intentionally excluded from version control.
