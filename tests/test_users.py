from jose import jwt
from app import schemas
from app.config import settings
import pytest
from tests.conftest import client, test_user_one


def test_root(client):
    response = client.get("/")
    # print(response.json().get("message"))
    assert response.json().get("message") == "Hello World"
    assert response.status_code == 200


def test_user_one_create(client):
    response = client.post(
        "/users/", json={"email": "testuser1@gmail.com", "password": "password123"}
    )

    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == "testuser1@gmail.com"
    assert response.status_code == 201


def test_login_user(client, test_user_one):
    response = client.post(
        "/login",
        data={
            "username": test_user_one["email"],
            "password": test_user_one["password"],
        },
    )

    login_response = schemas.Token(**response.json())
    payload = jwt.decode(
        login_response.access_token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )
    id = payload.get("user_id")
    assert id == test_user_one["id"]
    assert login_response.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("testuser1@gmail.com", "wrongPassword", 403),
        ("wrongGmail@gmail.com", "password123", 403),
        ("wrongGmail@gmail.com", "wrongPassword", 403),
        (None, "password123", 422),
        ("testuser1@gmail.com", None, 422),
    ],
)
def test_incorrect_login(client, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password})
    assert response.status_code == status_code
