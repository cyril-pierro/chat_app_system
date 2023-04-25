"""Sql Utility
Sql module to handle all sql operations
as a decorator or function 
"""

from functools import wraps
from typing import Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from error import exceptions
from tools import log


def sql_error_handler(func: object) -> object:
    """
    Check the error of an sql operation
    Args:
        func (object): func to decorate
    Returns:
        func
    Raises:
        UserOperationsError: raises user operation error
        ServerError: raises server error
    """

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IntegrityError as e:
            error_logger = log.Log(f"{func.__module__}.{func.__name__}")
            error_logger.exception(e.args[0])
            raise exceptions.UserOperationsError(msg="Username already exist")

        except Exception as e:
            error_logger = log.Log(f"{func.__module__}.{func.__name__}")
            error_logger.exception(e.args[0])
            raise exceptions.ServerError(msg="Error processing request")

    return inner


def add_object_to_database(db: Session, item: Any) -> bool:
    """
    Add an item to the database
    Args:
        db (object): contain the session for the
                database operations
        item(Any): The item to insert
    returns:
        bool
    """
    db.add(item)
    db.commit()
    db.refresh(item)
    return True