"""
SQLAlchemy models for users and todo items.

Description:
    This module defines the ORM tables used by the Todo application and their
    persisted fields.
"""

from database import Base

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Users(Base):
    """
    Represent an authenticated application user.

    Returns:
        A SQLAlchemy model mapped to the users table.
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)

    phone_number = Column(String)

    is_active = Column(Boolean, default=True)
    role = Column(String)

class Todos(Base):
    """
    Represent a todo item owned by a user.

    Returns:
        A SQLAlchemy model mapped to the todos table.
    """

    __tablename__ = 'todos'  
    
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)
    description = Column(String)
    priority = Column(Integer)

    complete = Column(Boolean, default=False, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"))
