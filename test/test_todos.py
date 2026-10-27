"""
Todo endpoint tests for the Todo application.

Description:
    This module verifies authenticated todo creation and lifecycle operations.
"""

from .utils import *

from ..database import get_db

from ..routers.auth import get_current_user
from starlette import status

from ..models import Todos

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all(test_demo_todo):

    """
    Verify read all behavior.
    """
    response = client.get("/todos/")
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
    response = client.get("/todos/todo/1")
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
    response = client.get("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
          'detail': 'Todo not found'
          }

def test_create_todo(test_demo_todo):

    """
    Verify create todo behavior.
    """
    request_data = {
          'title': 'New Demo todo',
          'description': 'New Demo todo',
          'priority': 5,
          'complete': False
          }

    response = client.post("/todos/todo", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')

def test_update_todo(test_demo_todo):

    """
    Verify update todo behavior.
    """
    request_data = {
          'title': 'Change Demo todo',
          'description': 'Change Demo todo',
          'priority': 5,
          'complete': False
          }

    response = client.put("/todos/todo/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')

def test_update_todo_not_found(test_demo_todo):

    """
    Verify update todo not found behavior.
    """
    request_data = {
              'title': 'Change Demo todo',
              'description': 'Change Demo todo',
              'priority': 5,
              'complete': False
              }

    response = client.put("/todos/todo/999", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
          'detail': 'Todo not found'
          }

def test_delete_todo(test_demo_todo):

    """
    Verify delete todo behavior.
    """
    response = client.delete("/todos/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_delete_todo_not_found(test_demo_todo):

    """
    Verify delete todo not found behavior.
    """
    response = client.delete("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
          'detail': 'Todo not found'
          }
