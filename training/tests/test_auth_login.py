import jwt
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from training.main import app
from training.config import settings
from training.schemas.user import User
from training.tests.factories import RoleSchemaFactory, UserSchemaFactory


client = TestClient(app)


@pytest.fixture
def admin_user() -> User:
    role = RoleSchemaFactory.build(name="Admin")
    user = UserSchemaFactory.build(roles=[role], report_agencies=[])
    return user


@pytest.fixture
def regular_user() -> User:
    user = UserSchemaFactory.build(roles=[], report_agencies=[])
    return user


@pytest.fixture
def admin_user_uaa_jwt(admin_user: User):
    return jwt.encode(admin_user.dict(), "test_uaa_key", algorithm="HS256")


@pytest.fixture
def regular_user_uaa_jwt(regular_user: User):
    return jwt.encode(regular_user.dict(), "test_uaa_key", algorithm="HS256")


@pytest.fixture
def invalid_jwt(admin_user: User):
    payload = admin_user.dict()
    payload["aud"] = [settings.AUTH_CLIENT_ID, "openid"]
    return jwt.encode(
        payload,
        "hakzors",
        algorithm="HS256",
        headers={"kid": "test_key_id"}
    )


def test_auth_metadata():
    response = client.get(
        "/api/v1/auth/metadata"
    )
    assert response.status_code == 200
    assert response.json()["authority"] == settings.AUTH_AUTHORITY_URL
    assert response.json()["client_id"] == settings.AUTH_CLIENT_ID


@patch("training.repositories.UserRepository.find_by_email")
@patch("training.api.auth.UAAJWTUser.decode_jwt")
def test_auth_exchange_valid_jwt_admin_user(decode_jwt, find_by_email, admin_user, admin_user_uaa_jwt):
    decode_jwt.return_value = admin_user.dict()
    find_by_email.return_value = admin_user

    response = client.post(
        "/api/v1/auth/exchange",
        headers={"Authorization": f"Bearer {admin_user_uaa_jwt}"}
    )
    assert response.status_code == 200


@patch("training.repositories.UserRepository.find_by_email")
@patch("training.api.auth.UAAJWTUser.decode_jwt")
def test_auth_exchange_valid_jwt_regular_user(decode_jwt, find_by_email, regular_user, regular_user_uaa_jwt):
    decode_jwt.return_value = regular_user.dict()
    find_by_email.return_value = regular_user

    response = client.post(
        "/api/v1/auth/exchange",
        headers={"Authorization": f"Bearer {regular_user_uaa_jwt}"}
    )
    assert response.status_code == 403


@patch("training.repositories.UserRepository.find_by_email")
@patch("training.api.auth.UAAJWTUser.decode_jwt")
def test_auth_exchange_valid_jwt_nonexistent_user(decode_jwt, find_by_email, regular_user, regular_user_uaa_jwt):
    decode_jwt.return_value = regular_user.dict()
    find_by_email.return_value = None

    response = client.post(
        "/api/v1/auth/exchange",
        headers={"Authorization": f"Bearer {regular_user_uaa_jwt}"}
    )
    assert response.status_code == 401


@patch("training.repositories.UserRepository.find_by_email")
@patch("training.api.auth.UAAJWTUser.get_jwks")
def test_auth_exchange_invalid_jwt(get_jwks, find_by_email, invalid_jwt, admin_user):
    get_jwks.return_value = {
        "test_key_id": {
            "key": "test_uaa_key",
            "alg": "HS256",
        }
    }
    find_by_email.return_value = admin_user

    response = client.post(
        "/api/v1/auth/exchange",
        headers={"Authorization": f"Bearer {invalid_jwt}"}
    )
    assert response.status_code == 403
