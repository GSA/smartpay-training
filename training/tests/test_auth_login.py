import jwt
import pytest
from unittest.mock import patch, MagicMock
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
    return jwt.encode(admin_user.model_dump(), "test_uaa_key", algorithm="HS256")


@pytest.fixture
def regular_user_uaa_jwt(regular_user: User):
    return jwt.encode(regular_user.model_dump(), "test_uaa_key", algorithm="HS256")


@pytest.fixture
def invalid_jwt(admin_user: User):
    payload = admin_user.model_dump()
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
    decode_jwt.return_value = admin_user.model_dump()
    find_by_email.return_value = admin_user

    response = client.post(
        "/api/v1/auth/exchange",
        headers={"Authorization": f"Bearer {admin_user_uaa_jwt}"}
    )
    assert response.status_code == 200


@patch("training.repositories.UserRepository.find_by_email")
@patch("training.api.auth.UAAJWTUser.decode_jwt")
def test_auth_exchange_invalid_scheme(decode_jwt, find_by_email, admin_user, admin_user_uaa_jwt):
    decode_jwt.return_value = admin_user.model_dump()
    find_by_email.return_value = admin_user

    response = client.post(
        "/api/v1/auth/exchange",
        headers={"Authorization": f"Non_Bearer {admin_user_uaa_jwt}"}
    )
    assert response.status_code == 403


@patch("training.repositories.UserRepository.find_by_email")
@patch("training.api.auth.UAAJWTUser.decode_jwt")
def test_auth_exchange_valid_jwt_regular_user(decode_jwt, find_by_email, regular_user, regular_user_uaa_jwt):
    decode_jwt.return_value = regular_user.model_dump()
    find_by_email.return_value = regular_user

    response = client.post(
        "/api/v1/auth/exchange",
        headers={"Authorization": f"Bearer {regular_user_uaa_jwt}"}
    )
    assert response.status_code == 403


@patch("training.repositories.UserRepository.find_by_email")
@patch("training.api.auth.UAAJWTUser.decode_jwt")
def test_auth_exchange_valid_jwt_nonexistent_user(decode_jwt, find_by_email, regular_user, regular_user_uaa_jwt):
    decode_jwt.return_value = regular_user.model_dump()
    find_by_email.return_value = None

    response = client.post(
        "/api/v1/auth/exchange",
        headers={"Authorization": f"Bearer {regular_user_uaa_jwt}"}
    )
    assert response.status_code == 403


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


@patch("training.repositories.UserRepository.find_by_email")
@patch("training.api.auth.UAAJWTUser.get_jwks")
def test_auth_exchange_no_jwk(get_jwks, find_by_email, invalid_jwt, admin_user):
    get_jwks.return_value = {}
    find_by_email.return_value = admin_user

    response = client.post(
        "/api/v1/auth/exchange",
        headers={"Authorization": f"Bearer {invalid_jwt}"}
    )
    assert response.status_code == 403


@patch("training.repositories.UserRepository.find_by_email")
@patch("training.api.auth.urlopen")
def test_auth_exchange_no_jwk_from_authority_url(fake_urlopen, find_by_email, invalid_jwt, admin_user):
    cm = MagicMock()
    cm.getcode.return_value = 200
    cm.read.return_value = '{}'
    cm.__enter__.return_value = cm
    fake_urlopen.return_value = cm

    find_by_email.return_value = admin_user

    response = client.post(
        "/api/v1/auth/exchange",
        headers={"Authorization": f"Bearer {invalid_jwt}"}
    )
    assert response.status_code == 503
    assert response.json() == {"detail": "Unable to get required data from authentication server (JWKS URI)."}


@patch("training.repositories.UserRepository.find_by_email")
@patch("training.api.auth.UAAJWTUser.discover_jwks_endpoint")
@patch("training.api.auth.urlopen")
def test_auth_exchange_no_keys_from_authority_url(fake_urlopen, discover_jwks_endpoint, find_by_email, invalid_jwt, admin_user):
    discover_jwks_endpoint.return_value = 'https://www.example.com'
    cm = MagicMock()
    cm.getcode.return_value = 200
    cm.read.return_value = '{}'
    cm.__enter__.return_value = cm
    fake_urlopen.return_value = cm

    find_by_email.return_value = admin_user

    response = client.post(
        "/api/v1/auth/exchange",
        headers={"Authorization": f"Bearer {invalid_jwt}"}
    )
    fake_urlopen.assert_called_once_with('https://www.example.com')
    assert response.status_code == 503
    assert response.json() == {"detail": "Unable to get required data from authentication server (public keys)."}
