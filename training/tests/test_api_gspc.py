import pytest
import jwt
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from training.main import app
from datetime import datetime, timedelta, timezone
from training.config import settings
from training.api.deps import gspc_invite_repository


client = TestClient(app)

ENDPOINT = "/api/v1/gspc-invite"


def post_gspc_invite(payload, goodJWT,):
    return client.post(
        ENDPOINT,
        json=payload,
        headers={"Authorization": f"Bearer {goodJWT}"}
    )


@pytest.fixture
def admin_user():
    return {
        'name': 'Albus Dumbledore',
        'email': 'dumbledore@hogwarts.edu',
        'roles': ['Admin']
    }


@pytest.fixture
def goodJWT(admin_user):
    return jwt.encode(admin_user, settings.JWT_SECRET, algorithm="HS256")


@pytest.fixture
def fake_gspc_invite_repo():
    mock = MagicMock()
    app.dependency_overrides[gspc_invite_repository] = lambda: mock
    yield mock
    app.dependency_overrides = {}


@pytest.fixture
def standard_payload():
    tomorrows_date = datetime.now(timezone.utc) + timedelta(days=1)

    return {
        "certification_expiration_date": tomorrows_date.strftime('%Y-%m-%dT00:00:00.000Z'),
        "email_addresses": "ValidEmail@test.com, ValidEmail2@test.com, invalidEmail, @invalidEmail.2"
    }


class TestGspc:
    @patch('training.config.settings', 'JWT_SECRET', 'super_secret')
    @patch('training.api.api_v1.gspc.send_gspc_invite_email')
    def test_gspc_invite_success(self, send_gspc_invite_email, goodJWT, standard_payload, fake_gspc_invite_repo):
        '''Given 2 valid emails it should call the db create method for each'''
        response = post_gspc_invite(standard_payload, goodJWT)

        assert response.status_code == 200
        assert fake_gspc_invite_repo.create.call_count == 2

    @patch('training.config.settings', 'JWT_SECRET', 'super_secret')
    @patch('training.api.api_v1.gspc.send_gspc_invite_email')
    def test_gspc_invite_parses_valid_emails(self, send_gspc_invite_email, goodJWT, standard_payload, fake_gspc_invite_repo):
        '''Given 2 valid emails in a list of 4 it should return a list of 2 valid emails'''
        response = post_gspc_invite(standard_payload, goodJWT)

        emailList = response.json()['valid_emails']
        assert len(emailList) == 2
        assert "ValidEmail@test.com" in emailList
        assert "ValidEmail2@test.com" in emailList

    @patch('training.config.settings', 'JWT_SECRET', 'super_secret')
    @patch('training.api.api_v1.gspc.send_gspc_invite_email')
    def test_gspc_invite_parses_invalid_emails(self, send_gspc_invite_email, goodJWT, standard_payload, fake_gspc_invite_repo):
        '''Given 2 invalid emails in a list of 4 it should return a list of 2 invalid emails'''
        response = post_gspc_invite(standard_payload, goodJWT)

        emailList = response.json()['invalid_emails']
        assert len(emailList) == 2
        assert "invalidEmail" in emailList
        assert "@invalidEmail.2" in emailList

    @patch('training.config.settings', 'JWT_SECRET', 'super_secret')
    @patch('training.api.api_v1.gspc.send_gspc_invite_email')
    def test_gspc_invite_sends_emails_to_valid_emails(self, goodJWT, standard_payload, fake_gspc_invite_repo):
        '''Given 2 valid emails send 2 invite emails'''
        with patch('training.api.api_v1.gspc.send_gspc_invite_email') as mock_send_email:
            post_gspc_invite(standard_payload, goodJWT)
            assert mock_send_email.call_count == 2

    @patch('training.config.settings', 'JWT_SECRET', 'super_secret')
    @patch('training.api.api_v1.gspc.send_gspc_invite_email')
    def test_gspc_invite_loggs_emails(self, send_gspc_invite_email, goodJWT, standard_payload, fake_gspc_invite_repo):
        '''Given 2 valid emails logger logs emails sent'''
        with patch('training.api.api_v1.gspc.logging') as logger:
            post_gspc_invite(standard_payload, goodJWT)
            assert logger.info.call_count == 2
