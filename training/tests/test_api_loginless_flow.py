import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from training.main import app
from training.data import UserCache
from training.api.deps import user_repository


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
def page_dest():
    return {"page_id": "travel_test", "title": "Amazing Training"}


class TestAuth:
    def test_email_only(self, user_email, page_dest, fake_cache, fake_user_repo):
        '''Should return a http 200 when user only sends email that is not in DB'''
        fake_cache.set.return_value = 'some_token'
        fake_user_repo.find_by_email.return_value = None
        response = client.post(
            "/api/v1/get-link",
            json={"user": user_email, "dest": page_dest},
        )
        print(response.text)
        assert response.status_code == 200
