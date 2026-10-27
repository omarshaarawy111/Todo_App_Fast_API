"""
Todo routes for creating, reading, updating, and deleting todo items.

Description:
    This module contains the HTML and API endpoints used by authenticated
    users to manage their todo items.
"""

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request

from pydantic import BaseModel, Field
from starlette import status

from typing import Annotated

from sqlalchemy.orm import Session

from ..models import Todos

from ..database import get_db

from .auth import get_current_user

from fastapi.templating import Jinja2Templates

from starlette.responses import HTMLResponse, RedirectResponse

router = APIRouter(
     prefix='/todos',
     tags=['todos']
)

templates = Jinja2Templates(directory="templates")

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
      """
      Validate fields used to create or update a todo item.
      """

      title: str = Field(min_length=3)
      description: str = Field(min_length=3, max_length=100)

      priority: int = Field(gt=0, lt=6)

      complete: bool = False

def redirect_to_login():
      """
      Build a redirect response for unauthenticated users.

      Returns:
          A redirect response with the stale access token removed.
      """

      redirect_response = RedirectResponse(url='/auth/login', status_code=status.HTTP_302_FOUND)

      redirect_response.delete_cookie(key="access_token")
      return redirect_response

@router.get(
    "/todo",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
)
async def render_todo_page(request: Request, db: db_dependency):
      """
      Render the todo list for the current user.

      Args:
          request: Incoming HTTP request.
          db: Database session.

      Returns:
          The rendered todo page or a login redirect.
      """

      token = request.cookies.get("access_token")
      if token is None:

            return redirect_to_login()

      try:
            user = await get_current_user(request.cookies.get("access_token"))
      except HTTPException:

            return redirect_to_login()

      if user.get("role") == "Admin":

            todos = db.query(Todos).all()
      else:

            todos = db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

      return templates.TemplateResponse("todo.html", {"request": request, "todos": todos, "user": user})

@router.get(
    "/add-todo",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
)
async def render_add_todo_page(request: Request):
      """
      Render the form used to create a todo item.

      Args:
          request: Incoming HTTP request.

      Returns:
          The rendered add-todo page or a login redirect.
      """

      token = request.cookies.get("access_token")
      if token is None:

            return redirect_to_login()

      try:
            user = await get_current_user(request.cookies.get("access_token"))
      except HTTPException:

            return redirect_to_login()

      return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})

@router.get(
    "/edit-todo/{todo_id}",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
)
async def render_edit_todo_page(request: Request, db: db_dependency, todo_id: int = Path(gt=0)):
      """
      Render the form used to edit an owned todo item.

      Args:
          request: Incoming HTTP request.
          db: Database session.
          todo_id: Todo identifier.

      Returns:
          The rendered edit page or a login redirect.
      """

      token = request.cookies.get("access_token")
      if token is None:

            return redirect_to_login()

      try:
            user = await get_current_user(request.cookies.get("access_token"))
      except HTTPException:

            return redirect_to_login()
      update_todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()

      return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": update_todo, "user": user})

@router.get('/', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
      """
      Return all todo items owned by the authenticated user.

      Args:
          user: Authenticated user claims.
          db: Database session.

      Returns:
          The user's todo items.
      """

      if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')

      return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

@router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt = 0)):
      """
      Return one todo item owned by the authenticated user.

      Args:
          user: Authenticated user claims.
          db: Database session.
          todo_id: Todo identifier.

      Returns:
          The requested todo item.
      """

      if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')
      todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
      if todo_model is not None:
            return todo_model
      raise HTTPException(status_code=404, detail='Todo not found')

@router.post('/todo', status_code=status.HTTP_204_NO_CONTENT)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
      """
      Create a todo item for the authenticated user.

      Args:
          user: Authenticated user claims.
          db: Database session.
          todo_request: Validated todo fields.
      """

      if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')

      new_todo = Todos(**todo_request.model_dump(), owner_id=user.get('id'))

      db.add(new_todo)

      db.commit()

@router.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
      """
      Update an existing todo item owned by the authenticated user.

      Args:
          user: Authenticated user claims.
          db: Database session.
          todo_request: Updated todo fields.
          todo_id: Todo identifier.
      """

      if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')
      update_todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
      if update_todo is None:
         raise HTTPException(status_code=404, detail='Todo not found')

      update_todo.title = todo_request.title
      update_todo.description = todo_request.description
      update_todo.priority = todo_request.priority
      update_todo.complete = todo_request.complete

      db.add(update_todo)

      db.commit()

@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
      """
      Delete a todo item owned by the authenticated user.

      Args:
          user: Authenticated user claims.
          db: Database session.
          todo_id: Todo identifier.
      """

      if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')
      delete_todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
      if delete_todo is None:
            raise HTTPException(status_code=404, detail='Todo not found')

      db.delete(delete_todo)

      db.commit()
