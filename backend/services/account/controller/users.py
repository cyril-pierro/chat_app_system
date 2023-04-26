"""User operations utility

This module contains the user allowed operations
"""

from typing import Union

from sqlalchemy import orm

from error import exceptions
from interfaces.users import UserOperationsInterface
from models.users import Users
from schemas import account, users
from utils import sql


class UserOperations(UserOperationsInterface):
    """User operations

    This class contains the various functions
    available to a user

    Attributes:
        _db (object): database session
            Session for database operations
    """

    def __init__(self, db: orm.Session) -> None:
        """Construct a User operation

        Args:
            db (object): database session
        Returns:
            None
        """
        self._db = db

    @sql.sql_error_handler
    def register_user(self, user: users.RegisterUser) -> Users:
        """Register a new User in the system

        Args:
            user (object): consist of the properties
            a user suppose to provide
        Returns:
            object
        """
        hash_password = Users.generate_hash_password(user.password)

        new_user = Users(
            username=user.username,
            hash_password=hash_password,  # type: ignore
            email=user.email,
        )
        sql.add_object_to_database(self._db, new_user)
        return new_user

    def verify_user(self, user: account.Login) -> int:
        """Check if a user exists in the system

        Args:
            user (object): consist of the properties
            a user suppose to provide
        Returns:
            object
        """
        user_found = self.get_user_by(user.username)
        verify_password = Users.verify_password(
            user_found.hash_password, user.password  # type: ignore
        )
        if not verify_password:
            raise exceptions.UserOperationsError(msg="Invalid password")
        return user_found.id

    def get_user_by(self, id_or_username: Union[str, int]) -> Users:
        """Get a user by either username or id

        Args:
            id_or_username (:str :int): consist of the properties
            a user suppose to provide
        Returns:
            object
        Raises:
            UserOperationError: raises Error
        """
        if isinstance(id_or_username, str):
            user_found = (
                self._db.query(Users)
                .filter(Users.username == id_or_username)  # type: ignore
                .first()
            )
        else:
            user_found = (
                self._db.query(Users)
                .filter(Users.id == id_or_username)  # type: ignore
                .first()
            )

        if user_found is None:
            raise exceptions.UserOperationsError(
                msg="User not found", status_code=404  # type: ignore
            )
        return user_found

    @sql.sql_error_handler
    def reset_user_password(self, id: int, password: str) -> None:
        """Change the password of a new User in the system
        Args:
            id (int): id of the user of the system
            password (str): password to use
        Returns:
            None
        """
        hash_password = Users.generate_hash_password(password)
        user_found = self.get_user_by(id)
        user_found.hash_password = hash_password
        sql.add_object_to_database(self._db, user_found)

    @sql.sql_error_handler
    def reset_user_email(self, user_id: int, email: str) -> None:
        """Change the email of a new User in the system

        Args:
            id (int): id of the user of the system
            email (str): email to use
        Returns:
            None
        """
        user_found = self.get_user_by(user_id)
        user_found.email = email
        sql.add_object_to_database(self._db, user_found)

    @sql.sql_error_handler
    def reset_user_username(self, user_id: int, username: str) -> None:
        """Change the username of a user in the system
        Args:
            id (int): id of the user of the system
            username (str):
        Returns:
            None
        """
        user_found = self.get_user_by(user_id)
        user_found.username = username
        sql.add_object_to_database(self._db, user_found)

    @sql.sql_error_handler
    def get_username(self, user_id: int) -> str:
        """Get the username of a user in the system
        Args:
            id (int): id of the user of the system
        Returns:
            str
        """
        user_found = self.get_user_by(user_id)
        return user_found.username
