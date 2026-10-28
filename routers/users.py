"""
User routes for account details and password management.

Description:
    This module exposes authenticated endpoints for viewing and updating the
    current user's account information.
"""

from fastapi import APIRouter, Depends, HTTPException, Path, Query

from pydantic import BaseModel, Field
from starlette import status

from typing import Annotated

from sqlalchemy.orm import Session

from models import Users

from database import get_db

from passlib.context import CryptContext

from auth import get_current_user, bcrypt_context

router = APIRouter(
     prefix='/users',
     tags=['users']
)

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]

class PasswordRequest(BaseModel):
    """
    Validate the old and new passwords for a password change.
    """

    old_password: str
    new_password: str

class PhoneNumberRequest(BaseModel):
    """
    Validate a new phone number for the current user.
    """

    phone_number: str

@router.get('/', status_code=status.HTTP_200_OK)
async def read_user_info(user: user_dependency, db: db_dependency):
    """
    Return the authenticated user's account information.

    Args:
        user: Authenticated user claims.
        db: Database session.

    Returns:
        The current user's database record.
    """

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def update_user_password(user: user_dependency, db: db_dependency, password_request: PasswordRequest):
    """
    Replace the authenticated user's password after verification.

    Args:
        user: Authenticated user claims.
        db: Database session.
        password_request: Current and replacement passwords.
    """

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    update_user = db.query(Users).filter(Users.id == user.get('id')).first()

    if update_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    if not bcrypt_context.verify(password_request.old_password, update_user.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')

    update_user.hashed_password = bcrypt_context.hash(password_request.new_password)

    db.add(update_user)

    db.commit()

@router.put('/phone-number', status_code=status.HTTP_204_NO_CONTENT)
async def update_user_phone_number(user: user_dependency, db: db_dependency, phone_number_request: PhoneNumberRequest):
    """
    Update the authenticated user's phone number.

    Args:
        user: Authenticated user claims.
        db: Database session.
        phone_number_request: Replacement phone number.
    """

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    update_user = db.query(Users).filter(Users.id == user.get('id')).first()

    if update_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    update_user.phone_number = phone_number_request.phone_number

    db.add(update_user)

    db.commit()
