"""
Shared fixtures and dependency overrides for application tests.

Description:
    This module provides test database sessions, authenticated user claims,
    and reusable todo and user fixtures.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from ..database import Base

from fastapi.testclient import TestClient

from ..main import app

import pytest

from ..models import Todos, Users

from ..routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

TestingSessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():

    """
    Provide a test database session to the application.
    """
    db = TestingSessionLocal()
    try:
      yield db
    finally:

      db.close()

def override_get_current_user():
   """
   Provide administrator claims for authenticated test requests.
   """
   return {'username': 'omar', 'id': 1, 'role': "Admin"}

client = TestClient(app)

@pytest.fixture
def test_demo_todo():

  """
  Verify demo todo behavior.
  """
  todo = Todos(
      title = 'Demo todo',
      description = 'Demo todo',
      priority = 5,
      complete = False,
      owner_id = 1
   )

  db = TestingSessionLocal()

  db.add(todo)

  db.commit()

  yield todo

  with engine.connect() as connection:

    connection.execute(text("DELETE FROM todos;"))

    connection.commit()

@pytest.fixture
def test_demo_user():

  """
  Verify demo user behavior.
  """
  user = Users(
      username = 'Demo user',
      email = 'Demo user',
      first_name = 'Demo user',
      last_name = 'Demo user',
      role = 'Admin',
      hashed_password = bcrypt_context.hash("1234"),
      is_active = True,
      phone_number = '1234'
   )

  db = TestingSessionLocal()

  db.add(user)

  db.commit()

  yield user

  with engine.connect() as connection:

    connection.execute(text("DELETE FROM users;"))

    connection.commit()
