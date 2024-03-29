"""Session
Context manager to maintain the
session of a database
"""

from functools import wraps

from sqlalchemy import orm

from core import setup


class DBSessionManager:
    """Database Session Manager"""

    def __init__(self):
        """Initialize the session manager"""
        self.db_init = setup.DatabaseSetup()
        self.db = self.db_init.get_session()

    def __enter__(self) -> orm.Session:
        """Return a database session"""
        return self.db()

    def __exit__(self, exc_type, exc_value, exc_trace):
        """Close the database session"""
        self.db().close()


def db_session(func):
    """Decorator for session management"""

    @wraps(func)
    def inner_function(*args, **kwargs):
        """Initialize the session"""
        with DBSessionManager() as db:
            kwargs["db"] = db
            return func(*args, **kwargs)

    return inner_function
