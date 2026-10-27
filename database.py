"""
Database configuration and session management for the Todo project.

Description:
    This module configures the SQLite engine, exposes the SQLAlchemy base
    class, and provides request-scoped database sessions.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Provide a database session for a request.

    Yields:
        An active SQLAlchemy session that is closed after request handling.
    """

    db = SessionLocal()
    try:
      yield db
    finally:

      db.close()
