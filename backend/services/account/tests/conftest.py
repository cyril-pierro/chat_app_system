"""Configuration for test

This module shows the configuration
done before you run a test

Attributes:
    SQLALCHEMY_DATABASE_URL (str): test database url
    engine (object): engine of the database
    SessionTesting (object): session of the database
"""
import os
import sys
from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.v1.router import account, users
from controller.account import AccountOperations
from controller.users import UserOperations
from core.setup import Base
from schemas.users import RegisterUser
from utils import sql

from . import test_data

# from utils.session import create


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# this is to include backend dir in sys.path so that we can import from db,main.py
os.environ.setdefault("TESTING", "True")


def start_application():
    app = FastAPI()
    app.include_router(users.router)
    app.include_router(account.router)
    return app


SQLALCHEMY_DATABASE_URL = "sqlite:///./testing.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

scope = "package"


@pytest.fixture(scope=scope)
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope=scope)
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope=scope)
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    # def _get_test_db():
    #     try:
    #         yield db_session
    #     finally:
    #         pass

    # app.dependency_overrides[create] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope=scope)
def user_operations():
    return UserOperations()


@pytest.fixture(scope=scope)
def account_operations():
    return AccountOperations()


@pytest.fixture(scope=scope)
def already_registered_user(user_operations):
    registered_user_data = test_data.test_user_data
    test_user = RegisterUser(**registered_user_data)
    registered_user = user_operations.register_user(test_user)
    user = user_operations.get_user_by(registered_user.username)
    user_operations.set_email_as_verified(user.id)
    user_verified = user_operations.get_user_by(user.username)
    return user_verified


@pytest.fixture(scope=scope)
def already_registered_user_unverified(user_operations):
    registered_user_data = test_data.test_user_unverified
    test_user = RegisterUser(**registered_user_data)
    registered_user = user_operations.register_user(test_user)
    return registered_user


@pytest.fixture(scope=scope)
def already_registered_admin(user_operations):
    registered_admin_data = test_data.test_admin_data
    test_user = RegisterUser(**registered_admin_data)
    registered_user = user_operations.register_user(test_user)
    admin = user_operations.get_user_by(registered_user.username)
    user_operations.set_email_as_verified(admin.id)
    registered_user.is_admin = True
    sql.add_object_to_database(registered_user)
    admin_verified = user_operations.get_user_by(admin.id)
    return admin_verified


@pytest.fixture(scope=scope)
def already_created_account(account_operations, already_registered_user):
    account_operations.create_account(already_registered_user.id)
    account = account_operations.get_account_with_user_id(already_registered_user.id)
    return account


@pytest.fixture(scope=scope)
def already_created_admin_account(account_operations, already_registered_admin):
    account_operations.create_account(already_registered_admin.id)
    account = account_operations.get_account_with_user_id(already_registered_admin.id)
    return account
