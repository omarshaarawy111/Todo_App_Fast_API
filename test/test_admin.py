"""
Administrative endpoint tests for the Todo application.

Description:
    This module verifies administrator access to todo records.
"""

from utils import *

from database import get_db

from routers.auth import get_current_user
from starlette import status

from models import Todos

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_users_todos(test_demo_todo):

    """
    Verify read all users todos behavior.
    """
    response = client.get("/admin/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
          {
          'id': 1,
          'title': 'Demo todo',
          'description': 'Demo todo',
          'priority': 5,
          'complete': False,
          'owner_id': 1
          }
          ]

def test_read_todo(test_demo_todo):

    """
    Verify read todo behavior.
    """
    response = client.get("/admin/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
          'id': 1,
          'title': 'Demo todo',
          'description': 'Demo todo',
          'priority': 5,
          'complete': False,
          'owner_id': 1
          }

def test_read_todo_not_found(test_demo_todo):

    """
    Verify read todo not found behavior.
    """
    response = client.get("/admin/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
          'detail': 'Todo not found'
          }

def test_delete_todo(test_demo_todo):

    """
    Verify delete todo behavior.
    """
    response = client.delete("/admin/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_delete_todo_not_found(test_demo_todo):

    """
    Verify delete todo not found behavior.
    """
    response = client.delete("/admin/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
          'detail': 'Todo not found'
          }
