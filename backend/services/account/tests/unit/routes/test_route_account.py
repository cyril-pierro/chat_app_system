import pytest
from fastapi_jwt_auth.exceptions import RevokedTokenError

import tests.test_data as test_data

LOGIN_URL = "/login"


@pytest.mark.route_accounts
def test_login_route(client, already_created_account):
    login_response = client.post(
        LOGIN_URL, json={"username": "testing_username", "password": "testing_123"}
    )
    assert login_response.status_code == 200


@pytest.mark.route_accounts
def test_refresh_route(client):
    login_response = client.post(
        LOGIN_URL, json={"username": "testing_username", "password": "testing_123"}
    )

    headers = {"Authorization": f"Bearer {login_response.json()['refresh_token']}"}
    refresh_response = client.post(
        "/refresh",
        json=test_data.test_login_data,
        headers=headers,
    )
    assert refresh_response.status_code == 200


@pytest.mark.route_accounts
def test_logout_route(client):
    login_response = client.post(
        LOGIN_URL, json={"username": "testing_username", "password": "testing_123"}
    )

    headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
    logout_response = client.post(
        "/logout",
        json=test_data.test_login_data,
        headers=headers,
    )
    assert logout_response.status_code == 200


@pytest.mark.route_accounts
def test_access_route_after_logout(client):
    login_response = client.post(
        LOGIN_URL, json={"username": "testing_username", "password": "testing_123"}
    )
    headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
    logout_response = client.post(
        "/logout",
        json=test_data.test_login_data,
        headers=headers,
    )
    assert logout_response.status_code == 200

    headers_1 = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
    with pytest.raises(RevokedTokenError):
        client.get(
            "/username",
            headers=headers_1,
        )
