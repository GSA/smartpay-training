import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from training.main import app
from training.data import UserCache
from training.api.deps import user_repository
from training.config import settings

client = TestClient(app)


@pytest.fixture
def fake_cache():
    mock = MagicMock()
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
def user_email():
    return {"email": "test@example.com"}


@pytest.fixture
def user_complete():
    return {"name": "Stephen Dedalus", "email": "test@example.com", "agency_id": 3}


@pytest.fixture
def page_dest():
    return {"pageId": "travel_test", "title": "Amazing Training"}


class TestAuth:
    def test_email_only(self, user_email, page_dest, fake_cache, fake_user_repo):
        '''Should return a http 200 when user only sends email that is not in DB'''
        fake_cache.set.return_value = 'some_token'
        fake_user_repo.find_by_email.return_value = None
        response = client.post(
            "/api/v1/get-link",
            json={"user": user_email, "dest": page_dest},
        )
        fake_user_repo.find_by_email.assert_called_with(user_email['email'])
        fake_cache.set.assert_not_called()
        assert response.status_code == 200

    @patch('training.api.api_v1.loginless_flow.send_email')
    def test_complete_user_sent(self, send_email, user_complete, page_dest, fake_cache, fake_user_repo):
        '''Should set the cache when a complete user object from the DB'''
        send_email.return_value = "email response"
        fake_cache.set.return_value = 'some_token'
        fake_user_repo.find_by_email.return_value = user_complete

        client.post(
            "/api/v1/get-link",
            json={"user": user_complete, "dest": page_dest},
        )
        fake_cache.set.assert_called_with(user_complete)

    @patch('training.api.api_v1.loginless_flow.send_email')
    def test_complete_user_http_201(self, send_email, user_complete, page_dest, fake_cache, fake_user_repo):
        '''Should return an HTTP 201 when creating an object in the cache'''
        send_email.return_value = "email response"
        fake_cache.set.return_value = 'some_token'
        fake_user_repo.find_by_email.return_value = user_complete

        response = client.post(
            "/api/v1/get-link",
            json={"user": user_complete, "dest": page_dest},
        )
        assert response.status_code == 201

    @patch('training.api.api_v1.loginless_flow.send_email')
    def test_complete_user_send_email(self, send_email, user_complete, page_dest, fake_cache, fake_user_repo):
        '''Should send email with the token in the link after setting the cache'''
        send_email.return_value = "email response"
        fake_cache.set.return_value = '123_some_token_1bc'
        fake_user_repo.find_by_email.return_value = user_complete
        url = f"{settings.BASE_URL}/quiz/{page_dest['page_id']}/?t=123_some_token_1bc"

        client.post(
            "/api/v1/get-link",
            json={"user": user_complete, "dest": page_dest},
        )

        send_email.assert_called_with(
            name=user_complete['name'],
            to_email=user_complete['email'],
            link=url,
            training_title=page_dest['title']
        )
