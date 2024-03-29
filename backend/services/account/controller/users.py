"""User operations utility

This module contains the user allowed operations
"""

from typing import Union

from sqlalchemy import orm

from error import exceptions
from interfaces.users import UserOperationsInterface
from models.users import Users
from schemas import account, users
from utils import session, sql


class UserOperations(UserOperationsInterface):
    """User operations

    This class contains the various functions
    available to a user

    Attributes:
        db (object): database session
            Session for database operations
    """

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
            hash_password=hash_password,
            email=user.email,
        )
        sql.add_object_to_database(item=new_user)
        return new_user

    def verify_user(self, user: account.Login) -> int:
        """Check if a user exists in the system

        Args:
            user (object): consist of the properties
            a user suppose to provide during login
        Returns:
            int
        """
        user_found = self.get_user_by(user.username)
        self.check_if_email_is_verified(user_found.id)

        verify_password = Users.verify_password(
            hash_password=user_found.hash_password, password=user.password
        )
        if not verify_password:
            raise exceptions.UserOperationsError(msg="Invalid credentials")
        user_id: int = user_found.id
        return user_id

    @session.db_session
    def get_user_by(
        self, id_or_username: Union[str, int], db: orm.Session = None
    ) -> Users:  # noqa
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
                db.query(Users).filter(Users.username == id_or_username).first()  # noqa
            )
        else:
            user_found = (
                db.query(Users).filter(Users.id == id_or_username).first()
            )  # noqa

        if user_found is None:
            raise exceptions.UserOperationsError(
                msg="Invalid Credentials", status_code=400
            )  # noqa
        return user_found

    @sql.sql_error_handler
    def reset_user_password(self, user_id: int, password: str) -> None:
        """Change the password of a new User in the system
        Args:
            user_id (int): id of the user of the system
            password (str): password to use
        Returns:
            None
        """
        hash_password = Users.generate_hash_password(password)
        user_found = self.get_user_by(user_id)
        user_found.hash_password = hash_password
        sql.add_object_to_database(item=user_found)

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
        sql.add_object_to_database(item=user_found)

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
        sql.add_object_to_database(item=user_found)

    @sql.sql_error_handler
    def get_username(self, user_id: int) -> str:
        """Get the username of a user in the system
        Args:
            id (int): id of the user of the system
        Returns:
            str
        """
        user_found = self.get_user_by(user_id)
        user_name: str = user_found.username
        return user_name

    @sql.sql_error_handler
    def set_email_as_verified(self, user_id: int) -> None:
        """Sets user email as verified
        Args:
            id (int): id of the user of the system
        Returns:
            None
        """
        user_found = self.get_user_by(user_id)
        user_found.is_email_verified = True
        sql.add_object_to_database(item=user_found)

    def check_if_email_is_verified(self, user_id: int) -> None:
        """Checks if the user email is verified
        Args:
            id (int): id of the user of the system
        Returns:
            None
        Raises:
            UserOperationError: Email not verified
        """
        user_found = self.get_user_by(user_id)
        if not user_found.is_email_verified:
            raise exceptions.UserOperationsError(
                msg="Email not verified", status_code=400
            )

    @sql.sql_error_handler
    def set_user_as_admin(self, user_id: int, admin_username: str) -> None:
        """Sets a user as an administrator
        Args:
            id (int): id of the user of the system
        Returns:
            None
        Raises:
            UserOperationsError: Error occurred
        """
        user_found = self.get_user_by(user_id)
        if not user_found.is_admin:
            raise exceptions.UserOperationsError(
                msg="Not Authorized for this operation",
                status_code=401,
            )
        assigned_admin = self.get_user_by(admin_username)
        assigned_admin.is_admin = True
        sql.add_object_to_database(item=assigned_admin)
