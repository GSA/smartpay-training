import pytest
from pydantic import EmailStr
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from training.main import app
from training.api.api_v1.loginless_flow import page_lookup
from training.data import UserCache
from training.schemas import User, TempUser, Role
from training.api.deps import user_repository
from training.config import settings

client = TestClient(app)


def fake_routes():
    return {
        'open_route': {'path': '/some_path/', 'required_roles': []},
        'auth_route': {'path': '/some_other_path/', 'required_roles': ['Wizard']},
        'auth_route_two': {'path': '/some_path/', 'required_roles': ['LizardMan']},
    }


@pytest.fixture(autouse=True)
def fake_page_lookup():
    mock = MagicMock()
    app.dependency_overrides[page_lookup] = fake_routes
    yield mock
    app.dependency_overrides = {}


@pytest.fixture(autouse=True)
def fake_cache():
    mock = MagicMock()
    mock.set.return_value = '123_some_token_1bc'
    app.dependency_overrides[UserCache] = lambda: mock
    yield mock
    app.dependency_overrides = {}


@pytest.fixture
def fake_user_repo():
    mock = MagicMock()
    app.dependency_overrides[user_repository] = lambda: mock
    yield mock
    app.dependency_overrides = {}


@pytest.fixture
def user_complete():
    return {"name": "Stephen Dedalus", "email": "test@example.com", "agency_id": 3, "roles": [], "report_agencies": []}


@pytest.fixture
def authorized_complete():
    return User(
        id=100,
        name="Stephen Dedalus",
        email=EmailStr("test@example.com"),
        agency_id=3,
        roles=[Role(id=1, name='Wizard')],
        report_agencies=[]
    )


class TestAuth:
    def test_unknown_page(self, fake_cache, fake_user_repo):
        '''Should return a http 400 when the requests asks to be forwarded to unknown page '''
        fake_user_repo.find_by_email.return_value = None

        response = client.post(
            "/api/v1/get-link",
            json={
                "user": {"email": "test@example.com"},
                "dest": {"page_id": "unknown_page_id", "title": "Doesn't Exist"}
            }
        )
        fake_cache.set.assert_not_called()
        assert response.status_code == 400

    def test_email_only(self, fake_cache, fake_user_repo):
        '''Should return a http 200 when user only sends email that is not in DB'''
        fake_user_repo.find_by_email.return_value = None
        response = client.post(
            "/api/v1/get-link",
            json={
                "user": {"email": "test@example.com"},
                "dest": {"page_id": "open_route", "title": "Public Page"}
            }
        )
        fake_user_repo.find_by_email.assert_called_with('test@example.com')
        fake_cache.set.assert_not_called()
        assert response.status_code == 200

    @patch('training.api.api_v1.loginless_flow.send_email')
    def test_auth_email_only(self, send_email, authorized_complete, fake_user_repo):
        '''Should return a http 201 when user only sends email that is in DB and has required role'''
        send_email.return_value = "email response"
        fake_user_repo.find_by_email.return_value = authorized_complete
        response = client.post(
            "/api/v1/get-link",
            json={
                "user": {"email": "test@example.com"},
                "dest": {"page_id": "auth_route", "title": "Non public but authorized page"}
            }
        )
        fake_user_repo.find_by_email.assert_called_with(authorized_complete.email)
        assert response.status_code == 201

    @patch('training.api.api_v1.loginless_flow.send_email')
    def test_bda_auth_email_only(self, send_email, authorized_complete, fake_user_repo):
        '''Should return a http 401 when user only sends email that is in DB and does not have required role'''
        send_email.return_value = "email response"
        fake_user_repo.find_by_email.return_value = authorized_complete
        response = client.post(
            "/api/v1/get-link",
            json={
                "user": {"email": "test@example.com"},
                "dest": {"page_id": "auth_route_two", "title": "Only for Lizard Men"}
            }
        )
        fake_user_repo.find_by_email.assert_called_with(authorized_complete.email)
        assert response.status_code == 401

    @patch('training.api.api_v1.loginless_flow.send_email')
    def test_complete_user_sent(self, send_email, user_complete, fake_cache, fake_user_repo):
        '''Should set the cache when a complete user object from the DB'''
        send_email.return_value = "email response"
        fake_user_repo.find_by_email.return_value = user_complete
        client.post(
            "/api/v1/get-link",
            json={
                "user": user_complete,
                "dest": {"page_id": "open_route", "title": "Public Page"}
            }
        )
        fake_cache.set.assert_called_with(TempUser(**user_complete))

    @patch('training.api.api_v1.loginless_flow.send_email')
    def test_complete_user_http_201(self, send_email, user_complete, fake_user_repo):
        '''Should return an HTTP 201 when creating an object in the cache'''
        send_email.return_value = "email response"
        fake_user_repo.find_by_email.return_value = user_complete

        response = client.post(
            "/api/v1/get-link",
            json={
                "user": user_complete,
                "dest": {"page_id": "open_route", "title": "Public Page"}
            }
        )
        assert response.status_code == 201

    @patch('training.api.api_v1.loginless_flow.send_email')
    def test_complete_user_send_email(self, send_email, user_complete, fake_user_repo):
        '''Should send email with the token in the link after setting the cache'''
        send_email.return_value = "email response"
        fake_user_repo.find_by_email.return_value = user_complete
        url = f"{settings.BASE_URL}/some_path/?t=123_some_token_1bc"

        client.post(
            "/api/v1/get-link",
            json={
                "user": user_complete,
                "dest": {"page_id": "open_route", "title": "Public Page"}
            }
        )

        send_email.assert_called_with(
            name=user_complete['name'],
            to_email=user_complete['email'],
            link=url,
            training_title='Public Page'
        )
