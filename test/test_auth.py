"""
Authentication and authorization tests for the Todo application.

Description:
    This module verifies user creation, token handling, and login behavior.
"""

from utils import *

from database import get_db

from routers.auth import authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, get_current_user

from jose import jwt, JWTError

from datetime import timedelta, datetime, timezone
from starlette import status

from models import Users

import pytest

from fastapi import HTTPException

app.dependency_overrides[get_db] = override_get_db

def test_create_user(test_demo_user):

    """
    Verify create user behavior.
    """
    request_data = {
            'email': 'New Demo user',
            'username': 'New Demo user',
            'first_name': 'New Demo user',
            'last_name': 'New Demo user',
            'password': '1234567',
            'phone_number': '1234567',
            'role': 'Admin',
            'is_active': True,
          }

    response = client.post("/auth/create-user", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Users).filter(Users.id == 2).first()
    assert model.email == request_data.get('email')
    assert model.username == request_data.get('username')
    assert model.first_name == request_data.get('first_name')
    assert model.last_name == request_data.get('last_name')

    assert bcrypt_context.verify(request_data['password'], model.hashed_password)
    assert model.phone_number == request_data.get('phone_number')
    assert model.role == request_data.get('role')
    assert model.is_active == request_data.get('is_active')

def test_authenticate_user(test_demo_user):

    """
    Verify authenticate user behavior.
    """
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_demo_user.username, '1234', db)

    assert authenticated_user is not None

    assert authenticated_user.username == test_demo_user.username

    wrong_user = authenticate_user('omar', '1234', db)
    assert wrong_user is False

    wrong_password = authenticate_user(test_demo_user.username, '1234567', db)
    assert wrong_password is False

def test_create_access_token(test_demo_user):

    """
    Verify create access token behavior.
    """
    username = test_demo_user.username
    user_id = 1
    role = test_demo_user.role
    expires_delta =  timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)

    encoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM, options={'verfity_signature': False})
    assert encoded_token['sub'] == username
    assert encoded_token['id'] == user_id
    assert encoded_token['role'] == role

@pytest.mark.asyncio
async def test_get_current_user(test_demo_user):

    """
    Verify get current user behavior.
    """
    username = test_demo_user.username
    user_id = 1
    role = test_demo_user.role

    encode = {
        "sub": username,
        "id": user_id,
        "role": role,
    }

    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    current_user = await get_current_user(token)
    assert current_user == {'username': test_demo_user.username, 'id': 1, 'role': test_demo_user.role}

@pytest.mark.asyncio
async def test_get_current_user_invalid_payload_token(test_demo_user):

    """
    Verify get current user invalid payload token behavior.
    """
    username = test_demo_user.username
    user_id = 1
    role = test_demo_user.role

    encode = {
        "sub": username
    }

    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == 'Invalid token payload'

@pytest.mark.asyncio
async def test_get_current_user_invalid_token(test_demo_user):

    """
    Verify get current user invalid token behavior.
    """
    invalid_token = "Invalid Token"

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=invalid_token)

    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == 'Invalid token'

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

def test_login_for_access_token(test_demo_user):

    """
    Verify login for access token behavior.
    """
    form_data = {
                  'username': test_demo_user.username,
                  'password': '1234'
                }

    username = test_demo_user.username
    user_id = 1
    role = test_demo_user.role
    response = client.post("/auth/token", data = form_data)
    assert response.status_code == status.HTTP_200_OK

    token = response.json()['access_token']

    encoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM, options={'verfity_signature': False})
    assert encoded_token['sub'] == username
    assert encoded_token['id'] == user_id
    assert encoded_token['role'] == role

    assert response.json()['token_type'] == 'bearer'

def test_login_for_access_token(test_demo_user):

    """
    Verify login for access token behavior.
    """
    form_data = {
                  'username': 'Wrong Demo User',
                  'password': '1234'
                }

    username = test_demo_user.username
    response = client.post("/auth/token", data = form_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
          'detail': 'Incorrect username or password'
          }

def test_login_for_access_token(test_demo_user):

    """
    Verify login for access token behavior.
    """
    form_data = {
                  'username': test_demo_user.username,
                  'password': '1234567'
                }

    username = test_demo_user.username
    response = client.post("/auth/token", data = form_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
          'detail': 'Incorrect username or password'
          }
