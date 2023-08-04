from fastapi import FastAPI, Depends
from unittest.mock import patch
from fastapi.testclient import TestClient
import jwt
import pytest

from training.api.auth import JWTUser, RequireRole, user_from_form
from training.config import settings


app = FastAPI()


@pytest.fixture
def user():
    return {
        'name': 'Leopold Bloom',
        'email': 'lbloom@sandymount.com',
        'roles': ['aopc', 'wizard']
    }


@pytest.fixture
def non_auth_user():
    return {
        'name': 'Leopold Bloom',
        'email': 'lbloom@sandymount.com',
        'roles': ['user', 'wizard']
    }


@pytest.fixture
def no_roles_user():
    return {
        'name': 'Leopold Bloom',
        'email': 'lbloom@sandymount.com',
    }


@pytest.fixture
def goodJWT(user):
    return jwt.encode(user, settings.JWT_SECRET, algorithm="HS256")


@pytest.fixture
def nonAuthJWT(non_auth_user):
    return jwt.encode(non_auth_user, settings.JWT_SECRET, algorithm="HS256")


@pytest.fixture
def badJWT(user):
    return jwt.encode(user, 'hakzors', algorithm="HS256")


@pytest.fixture
def noRoleJWT(no_roles_user):
    return jwt.encode(no_roles_user, settings.JWT_SECRET, algorithm="HS256")


@app.get("/home")
def read_current_user(user=Depends(JWTUser())):
    return user


@app.get("/auth_required")
def read_role(user=Depends(RequireRole(['aopc']))):
    return user


@app.get("/auth_required_multi")
def read_multiple_role(user=Depends(RequireRole(['aopc', 'wizard']))):
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

    def test_valid_role(self, goodJWT, user):
        response = client.get("/auth_required", headers={"Authorization": f"Bearer {goodJWT}"})
        assert response.status_code == 200
        assert response.json() == user

    def test_user_without_proper_role(self, nonAuthJWT):
        response = client.get("/auth_required", headers={"Authorization": f"Bearer {nonAuthJWT}"})
        assert response.status_code == 401
        assert response.json() == {'detail': 'Not Authorized'}

    def test_route_multiple_role(self, goodJWT, user):
        response = client.get("/auth_required_multi", headers={"Authorization": f"Bearer {goodJWT}"})
        assert response.status_code == 200
        assert response.json() == user

    def test_route_all_roles(self, nonAuthJWT):
        '''user must have all roles associate with a route'''
        response = client.get("/auth_required_multi", headers={"Authorization": f"Bearer {nonAuthJWT}"})
        assert response.status_code == 401
        assert response.json() == {'detail': 'Not Authorized'}

    def test_jwt_without_roles(self, noRoleJWT):
        '''jwt without roles is just a 401'''
        response = client.get("/auth_required_multi", headers={"Authorization": f"Bearer {noRoleJWT}"})
        assert response.status_code == 401
        assert response.json() == {'detail': 'Not Authorized'}

    def test_jwt_without_roles_okay_when_not_needed(self, noRoleJWT, no_roles_user):
        '''jwt without roles still work if roles are not required'''
        response = client.get("/home", headers={"Authorization": f"Bearer {noRoleJWT}"})
        assert response.status_code == 200
        assert response.json() == no_roles_user


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
