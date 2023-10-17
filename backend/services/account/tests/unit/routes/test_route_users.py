import os

import pytest

from tests import test_data

LOGIN_URL = "/login"


@pytest.mark.route_users
@pytest.mark.parametrize(
    "expected_json", [({"username": "test_user", "email": "test_email@test.com"})]
)
def test_register_route(client, expected_json):
    response = client.post("/register", json=test_data.test_user_data)
    assert response.json() == expected_json
    assert response.status_code == 200


@pytest.mark.route_users
def test_change_email_route(client, user_operations, account_operations):
    new_email = "test1@email.com"
    username = test_data.test_login_data.get("username")
    user = user_operations.get_user_by(username)
    user_operations.set_email_as_verified(user.id)
    account_operations.create_account(user.id)

    login_response = client.post("/login", json=test_data.test_login_data)

    headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
    # change email
    change_email_response = client.post(
        "/change/email", headers=headers, json={"email": new_email}
    )
    assert change_email_response.status_code == 200
    assert change_email_response.json() == {"message": "email changed successfully"}


@pytest.mark.route_users
def test_change_username_route(client):
    login_response = client.post(LOGIN_URL, json=test_data.test_login_data)

    new_username = "test_new_username"

    headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
    # change username
    change_username_response = client.post(
        "/change/username", headers=headers, json={"username": new_username}
    )
    assert change_username_response.status_code == 200
    assert change_username_response.json() == {
        "message": "username changed successfully"
    }


@pytest.mark.route_users
def test_change_password_route(client):
    login_response = client.post(
        LOGIN_URL, json={"username": "test_new_username", "password": "test_password"}
    )
    new_password = "test_user_password"
    headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
    # get password
    change_password_response = client.post(
        "/change/password",
        headers=headers,
    )

    assert change_password_response.status_code == 200

    # change password
    headers_2 = {
        "Authorization": f"Bearer {change_password_response.json()['access_token']}"
    }

    change_password_confirm_response = client.post(
        "/change/password/confirm", headers=headers_2, json={"password": new_password}
    )

    assert change_password_confirm_response.status_code == 200
    assert change_password_confirm_response.json() == {
        "message": "changed password successfully"
    }


@pytest.mark.route_users
def test_admin_route(client):
    admin_username = os.environ["ADMIN_USERNAME"]
    admin_password = os.environ["ADMIN_PASSWORD"]

    login_response = client.post(
        LOGIN_URL, json={"username": admin_username, "password": admin_password}
    )
    headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}

    add_admin_response = client.post(
        "/admin",
        json={"username": "test_new_username"},
        headers=headers,
    )
    assert add_admin_response.status_code == 200
