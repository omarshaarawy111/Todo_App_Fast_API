"""
User endpoint tests for the Todo application.

Description:
    This module verifies user information and account update operations.
"""

from utils import *

from database import get_db

from routers.auth import get_current_user
from starlette import status

from ..models import Users

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_user_info(test_demo_user):

    """
    Verify read user info behavior.
    """
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert bcrypt_context.verify('1234', response_data['hashed_password'])

    response_data.pop('hashed_password')
    assert response_data == {
          'id': 1,
          'email': 'Demo user',
          'username': 'Demo user',
          'first_name': 'Demo user',
          'last_name': 'Demo user',
          'phone_number': '1234',
          'is_active': True,
          'role': 'Admin'

          }

def test_update_user_password(test_demo_user):

    """
    Verify update user password behavior.
    """
    password_request = {
              'old_password': '1234',
              'new_password': '12345'
            }

    response = client.put("/users/password", json=password_request)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Users).filter(Users.id == 1).first()

    assert bcrypt_context.verify(password_request['new_password'], model.hashed_password)

def test_update_user_password_invalid(test_demo_user):

    """
    Verify update user password invalid behavior.
    """
    password_request = {
                  'old_password': '1234567',
                  'new_password': '12345'
                }

    response = client.put("/users/password", json=password_request)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
          'detail': 'Error on password change'
          }

def test_update_user_phone_number(test_demo_user):

    """
    Verify update user phone number behavior.
    """
    request_data = {
              'phone_number': '12345'
            }

    response = client.put("/users/phone-number", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Users).filter(Users.id == 1).first()

    assert request_data['phone_number'] == model.phone_number
