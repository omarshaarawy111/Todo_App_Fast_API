"""
FastAPI application entry point for the Todo project.

Description:
    This module creates the application, configures static assets, initializes
    the database schema, and registers the application routers.
"""

from fastapi import FastAPI, Request

from fastapi.responses import HTMLResponse

from models import Base
from starlette import status

from routers import auth, todos, admin, users

from database import engine

from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

Base.metadata.create_all(bind=engine)

@app.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
)
def test_template(request: Request):
    """
    Redirect the application root to the todo page.

    Args:
        request: Incoming HTTP request.

    Returns:
        A redirect response to the todo page.
    """

    return RedirectResponse(url="/todos/todo", status_code=status.HTTP_302_FOUND)

@app.get("/healthy", status_code=status.HTTP_200_OK)
def health_check():
    """
    Report the availability of the application.

    Returns:
        A health status response.
    """
    return {'Status': 'Healthy'}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
