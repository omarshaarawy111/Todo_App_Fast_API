"""
Administrative routes for the Todo application.

Description:
    This module provides endpoints used to manage application users and
    enforce administrator access.
"""

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from starlette import status

from typing import Annotated

from sqlalchemy.orm import Session

from models import Todos

from database import get_db

from auth import get_current_user

router = APIRouter(
     prefix='/admin',
     tags=['admin']
)

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/', status_code=status.HTTP_200_OK)
async def read_all_users_todos(user: user_dependency, db: db_dependency):
      """
      Return all todo items for an administrator.

      Args:
          user: Authenticated administrator claims.
          db: Database session.

      Returns:
          All todo items in the database.
      """

      if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')
      if user.get("role")!= "Admin":
            raise HTTPException(status_code=401, detail='Permission is denied')

      return db.query(Todos).all()

@router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt = 0)):
      """
      Return any todo item for an administrator.

      Args:
          user: Authenticated administrator claims.
          db: Database session.
          todo_id: Todo identifier.

      Returns:
          The requested todo item.
      """

      if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')
      if user.get("role")!= "Admin":
            raise HTTPException(status_code=401, detail='Permission is denied')
      todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
      if todo_model is not None:
            return todo_model
      raise HTTPException(status_code=404, detail='Todo not found')

@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
      """
      Delete any todo item for an administrator.

      Args:
          user: Authenticated administrator claims.
          db: Database session.
          todo_id: Todo identifier.
      """

      if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')
      if user.get("role")!= "Admin":
            raise HTTPException(status_code=401, detail='Permission is denied')
      delete_todo = db.query(Todos).filter(Todos.id == todo_id).first()
      if delete_todo is None:
            raise HTTPException(status_code=404, detail='Todo not found')

      db.delete(delete_todo)

      db.commit()
