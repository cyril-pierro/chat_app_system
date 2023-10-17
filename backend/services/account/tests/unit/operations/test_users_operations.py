import os

import pytest

from error import exceptions
from models.users import Users
from schemas.account import Login
from schemas.users import RegisterUser

from ... import test_data


@pytest.mark.user_operations
@pytest.mark.parametrize("register_user_data", [(test_data.test_register_user)])
def test_register_user(user_operations, register_user_data):
    test_user = RegisterUser(**register_user_data)
    saved_user = user_operations.register_user(test_user)

    # saved operations
    assert saved_user.username == test_user.username
    assert Users.verify_password(saved_user.hash_password, test_user.password)
    assert saved_user.email == test_user.email

    # user string representation
    assert str(saved_user) == f"{saved_user.id}-{saved_user.username}"


@pytest.mark.user_operations
@pytest.mark.parametrize("login_data", [(test_data.test_login_data)])
def test_verify_user(user_operations, login_data):
    login_user_scheme = Login(**login_data)
    user = user_operations.get_user_by(login_user_scheme.username)
    user_operations.set_email_as_verified(user.id)
    login_user_id = user_operations.verify_user(login_user_scheme)
    assert login_user_id == user.id


@pytest.mark.user_operations
def test_get_user_by_username(user_operations):
    username = test_data.test_user_data.get("username")
    get_user_if_user_exists = user_operations.get_user_by(username)
    assert get_user_if_user_exists.username == username


@pytest.mark.user_operations
def test_get_user_by_id(user_operations):
    username = test_data.test_user_data.get("username")
    get_user_by_name = user_operations.get_user_by(username)
    get_user_if_user_exists = user_operations.get_user_by(get_user_by_name.id)
    assert get_user_if_user_exists.id == get_user_by_name.id


@pytest.mark.user_operations
def test_get_user_by_raises_exception(user_operations):
    with pytest.raises(exceptions.UserOperationsError):
        user_not_registered_username = "not_registered_username"
        _ = user_operations.get_user_by(user_not_registered_username)


@pytest.mark.user_operations
def test_invalid_password(user_operations):
    with pytest.raises(exceptions.UserOperationsError):
        username = test_data.test_user_data.get("username")
        password = "fake_password"
        login_data = {"username": username, "password": password}
        login_user_scheme = Login(**login_data)
        user_operations.verify_user(login_user_scheme)


@pytest.mark.user_operations
def test_unauthorized_registration(user_operations):
    with pytest.raises(exceptions.UserOperationsError):
        username = test_data.test_user_data.get("username")
        user = user_operations.get_user_by(username)
        user_operations.set_user_as_admin(user.id, "fake_admin")


@pytest.mark.user_operations
def test_reset_user_password(user_operations):
    new_password = "testing_123"
    username = test_data.test_user_data.get("username")
    get_user_if_user_exists = user_operations.get_user_by(username)
    user_operations.reset_user_password(get_user_if_user_exists.id, new_password)
    get_user_after_password_reset = user_operations.get_user_by(username)
    assert Users.verify_password(
        get_user_after_password_reset.hash_password, new_password
    )


@pytest.mark.user_operations
def test_reset_user_username(user_operations):
    new_username = "testing_username"
    username = test_data.test_user_data.get("username")
    get_user_if_user_exists = user_operations.get_user_by(username)
    user_operations.reset_user_username(get_user_if_user_exists.id, new_username)
    get_user_after_username_reset = user_operations.get_user_by(new_username)
    get_user_if_user_exists = user_operations.get_user_by(
        get_user_after_username_reset.id
    )

    assert get_user_if_user_exists.username == new_username


@pytest.mark.user_operations
def test_reset_user_email(user_operations):
    new_email = "testing@gmail.com"
    username = "testing_username"
    get_user_if_user_exists = user_operations.get_user_by(username)
    user_operations.reset_user_email(get_user_if_user_exists.id, new_email)
    get_user_after_email_reset = user_operations.get_user_by(get_user_if_user_exists.id)
    assert get_user_after_email_reset.email == new_email


@pytest.mark.user_operations
def test_get_username(already_registered_user):
    assert already_registered_user.username == test_data.test_user_data.get("username")


@pytest.mark.user_operations
def test_set_email_as_verified(user_operations, already_registered_user):
    user_operations.set_email_as_verified(already_registered_user.id)

    found_user = user_operations.get_user_by(already_registered_user.id)

    assert found_user.is_email_verified


@pytest.mark.user_operations
def test_check_if_email_is_verified_error(
    user_operations, already_registered_user_unverified
):
    with pytest.raises(exceptions.UserOperationsError):
        user_operations.check_if_email_is_verified(
            already_registered_user_unverified.id
        )


@pytest.mark.user_operations
def test_set_user_as_admin(
    user_operations,
):
    username = os.environ["ADMIN_USERNAME"]
    get_admin_details_if_exists = user_operations.get_user_by(username)
    username = "testing_username"
    get_user_if_user_exists = user_operations.get_user_by(username)
    user_operations.set_user_as_admin(
        get_admin_details_if_exists.id, get_user_if_user_exists.username
    )
    user_found = user_operations.get_user_by(get_user_if_user_exists.id)
    assert user_found.is_admin == True
