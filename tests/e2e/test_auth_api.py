import pytest
from pydantic import ValidationError

from app.schemas.users import UserWithRoleSchema


def test_user_login(not_logged_client):
    client = not_logged_client
    resp = client.post("/auth/login", json={
        "username": "just_a_user",
        "password": "123"
    })

    assert resp.status_code == 200
    assert resp.json == {"message": "Authentication done successfully."}


def test_user_login_bad_credentials(not_logged_client):
    client = not_logged_client
    resp = client.post("/auth/login", json={
        "username": "another",
        "password": "123"
    })

    assert resp.status_code == 400
    assert resp.json == {"message": "Incorrect username or password."}


def test_user_login_bad_request(not_logged_client):
    client = not_logged_client
    resp = client.post("/auth/login", json={})

    assert resp.status_code == 400
    assert resp.json == {"message": "Username and password is required fields."}


def test_user_register(not_logged_client):
    client = not_logged_client
    resp = client.post("/auth/register", json={
        "username": "new_user",
        "password": "123"
    })

    assert resp.status_code == 200
    assert resp.json == {"message": "Registered successfully."}


def test_user_register_username_already_exists(not_logged_client):
    client = not_logged_client
    resp = client.post("/auth/register", json={
        "username": "admin",
        "password": "123"
    })

    assert resp.status_code == 400
    assert resp.json == {"message": "Username is already used."}


def test_user_register_bad_request(not_logged_client):
    client = not_logged_client
    resp = client.post("/auth/register", json={})

    assert resp.status_code == 400
    assert resp.json == {"message": "Username and password is required fields."}


def test_user_logout(logged_client):
    client = logged_client
    resp = client.post("/auth/logout")

    assert resp.status_code == 200
    assert resp.json == {"message": "Logout done successfully."}


def test_user_logout_with_no_logged(not_logged_client):
    client = not_logged_client
    resp = client.post("/auth/logout")

    assert resp.status_code == 401
    assert resp.json == {"message": "Unauthenticated."}


def test_user_info(logged_client):
    client = logged_client
    resp = client.get("/auth/user")

    assert resp.status_code == 200

    try:
        UserWithRoleSchema.parse_obj(resp.json)
    except ValidationError:
        pytest.fail("Incorrect user info route response.")


def test_user_info_with_no_logged(not_logged_client):
    client = not_logged_client
    resp = client.get("/auth/user")

    assert resp.status_code == 401
    assert resp.json == {"message": "Unauthenticated."}
