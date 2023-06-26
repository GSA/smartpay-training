import jwt
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from training import models
from training.main import app
from training.config import settings
from training.tests.factories import RoleSchemaFactory, UserSchemaFactory


client = TestClient(app)


@pytest.fixture
def admin_user_data() -> dict:
    admin_role = RoleSchemaFactory.build(name="Admin")
    admin_user = UserSchemaFactory.build(roles=[admin_role], report_agencies=[])
    return admin_user.dict()


@pytest.fixture
def regular_user_data() -> dict:
    regular_user = UserSchemaFactory.build(report_agencies=[])
    return regular_user.dict()


@pytest.fixture
def admin_user_uaa_jwt(admin_user_data):
    return jwt.encode(admin_user_data, "test_uaa_key", algorithm="HS256")


@pytest.fixture
def regular_user_uaa_jwt(regular_user_data):
    return jwt.encode(regular_user_data, "test_uaa_key", algorithm="HS256")


@pytest.fixture
def invalid_jwt(admin_user_data: dict):
    payload = admin_user_data.copy()
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
def test_auth_exchange_valid_jwt_admin_user(decode_jwt, find_by_email, admin_user_data, admin_user_uaa_jwt):
    decode_jwt.return_value = dict(admin_user_data)
    find_by_email.return_value = models.User(**admin_user_data)

    response = client.post(
        "/api/v1/auth/exchange",
        headers={"Authorization": f"Bearer {admin_user_uaa_jwt}"}
    )
    assert response.status_code == 200


@patch("training.repositories.UserRepository.find_by_email")
@patch("training.api.auth.UAAJWTUser.decode_jwt")
def test_auth_exchange_valid_jwt_regular_user(decode_jwt, find_by_email, regular_user_data, regular_user_uaa_jwt):
    decode_jwt.return_value = dict(regular_user_data)
    find_by_email.return_value = models.User(**regular_user_data)

    response = client.post(
        "/api/v1/auth/exchange",
        headers={"Authorization": f"Bearer {regular_user_uaa_jwt}"}
    )
    assert response.status_code == 403


@patch("training.repositories.UserRepository.find_by_email")
@patch("training.api.auth.UAAJWTUser.decode_jwt")
def test_auth_exchange_valid_jwt_nonexistent_user(decode_jwt, find_by_email, regular_user_data, regular_user_uaa_jwt):
    decode_jwt.return_value = dict(regular_user_data)
    find_by_email.return_value = None

    response = client.post(
        "/api/v1/auth/exchange",
        headers={"Authorization": f"Bearer {regular_user_uaa_jwt}"}
    )
    assert response.status_code == 401


@patch("training.repositories.UserRepository.find_by_email")
@patch("training.api.auth.UAAJWTUser.get_jwks")
def test_auth_exchange_invalid_jwt(get_jwks, find_by_email, invalid_jwt, admin_user_data):
    get_jwks.return_value = {
        "test_key_id": {
            "key": "test_uaa_key",
            "alg": "HS256",
        }
    }
    find_by_email.return_value = models.User(**admin_user_data)

    response = client.post(
        "/api/v1/auth/exchange",
        headers={"Authorization": f"Bearer {invalid_jwt}"}
    )
    assert response.status_code == 403
