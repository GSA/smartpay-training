from fastapi import FastAPI, Depends
from unittest.mock import patch
from fastapi.testclient import TestClient
import jwt
import pytest

from training.api.auth import JWTUser, user_from_form
from training.config import settings


app = FastAPI()


@pytest.fixture
def user():
    return {
        'name': 'Leopold Bloom',
        'email': 'lbloom@sandymount.com'
    }


@pytest.fixture
def goodJWT(user):
    return jwt.encode(user, settings.JWT_SECRET, algorithm="HS256")


@pytest.fixture
def badJWT(user):
    return jwt.encode(user, 'hakzors', algorithm="HS256")


@app.get("/home")
def read_current_user(user=Depends(JWTUser())):
    return user


@app.post("/home")
def read_current_user_from_form(user=Depends(user_from_form)):
    return user


client = TestClient(app)


@patch('training.config.settings', 'JWT_SECRET', 'super_secret')
class TestAuth:
    def test_valid_jwt(self, goodJWT, user):
        response = client.get("/home", headers={"Authorization": f"Bearer {goodJWT}"})
        assert response.status_code == 200
        assert response.json() == user

    def test_invalid_jwt(self, badJWT):
        response = client.get("/home", headers={"Authorization": f"Bearer {badJWT}"})
        assert response.status_code == 403
        assert response.json() == {'detail': 'Invalid or expired token.'}

    def test_missing_jwt(self):
        response = client.get("/home")
        assert response.status_code == 403
        assert response.json() == {'detail': 'Not authenticated'}


@patch('training.config.settings', 'JWT_SECRET', 'super_secret')
class TestUserFromFormField:
    def test_valid_jwt(self, goodJWT, user):
        response = client.post("/home", data={"jwtToken": goodJWT})
        assert response.status_code == 200
        assert response.json() == user

    def test_inalid_jwt(self, badJWT):
        response = client.post("/home", data={"jwtToken": badJWT})
        assert response.status_code == 401

    def test_no_jwt(self):
        # without expected data FastAPI returns 422 Unprocessable Entity
        response = client.post("/home", data={})
        assert response.status_code == 422
