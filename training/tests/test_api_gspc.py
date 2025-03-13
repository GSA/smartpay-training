import pytest
import jwt
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from training.main import app
from datetime import datetime, timedelta, timezone
from training.config import settings
from training.api.deps import gspc_invite_repository, gspc_completion_repository
from http import HTTPStatus


client = TestClient(app)

GSPC_INVITE_ENDPOINT = "/api/v1/gspc/send-invites"
GSPC_REPORT_ENDPOINT = "/api/v1/gspc/download-gspc-completion-report"
GSPC_FOLLOW_UP_ENDPOINT = "/api/v1/gspc/send-follow-ups"


def post_gspc_invite(payload, goodJWT,):
    return client.post(
        GSPC_INVITE_ENDPOINT,
        json=payload,
        headers={"Authorization": f"Bearer {goodJWT}"}
    )


def post_gspc_report(goodJWT):
    return client.post(
        GSPC_REPORT_ENDPOINT,
        headers={"Authorization": f"Bearer {goodJWT}"}
    )


def post_gspc_follow_up(goodJWT):
    return client.post(
        GSPC_FOLLOW_UP_ENDPOINT,
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
def standard_user():
    return {
        'name': 'Albus Dumbledore',
        'email': 'dumbledore@hogwarts.edu',
        'roles': ['']
    }


@pytest.fixture
def goodJWT(admin_user):
    return jwt.encode(admin_user, settings.JWT_SECRET, algorithm="HS256")


@pytest.fixture
def badJWT(standard_user):
    return jwt.encode(standard_user, settings.JWT_SECRET, algorithm="HS256")


@pytest.fixture
def fake_gspc_invite_repo():
    mock = MagicMock()
    app.dependency_overrides[gspc_invite_repository] = lambda: mock
    yield mock
    app.dependency_overrides = {}


@pytest.fixture
def fake_gspc_completion_repository():
    mock = MagicMock()
    app.dependency_overrides[gspc_completion_repository] = lambda: mock
    yield mock
    app.dependency_overrides = {}


@pytest.fixture
def standard_payload():
    tomorrows_date = datetime.now(timezone.utc) + timedelta(days=1)

    return {
        "certification_expiration_date": tomorrows_date.strftime('%Y-%m-%dT00:00:00.000Z'),
        "email_addresses": "ValidEmail@test.com, ValidEmail2@test.com, invalidEmail, @invalidEmail.2"
    }


@pytest.fixture
def mock_follow_up_invites():
    class MockInvite:
        def __init__(self, gspc_invite_id, email):
            self.gspc_invite_id = gspc_invite_id
            self.email = email

    second_follow_ups = [
        MockInvite("123", "second1@test.com"),
        MockInvite("456", "second2@test.com")
    ]

    final_follow_ups = [
        MockInvite("789", "final1@test.com"),
        MockInvite("012", "final2@test.com")
    ]

    return {
        "second": second_follow_ups,
        "final": final_follow_ups
    }


class TestGspc:
    @patch('training.config.settings', 'JWT_SECRET', 'super_secret')
    @patch('training.api.api_v1.gspc.send_gspc_invite_emails')
    def test_gspc_invite_success(self, gspc_admin_invite, goodJWT, standard_payload, fake_gspc_invite_repo):
        '''Given 2 valid emails it should call the db create method for each'''
        response = post_gspc_invite(standard_payload, goodJWT)

        assert response.status_code == HTTPStatus.OK
        assert fake_gspc_invite_repo.bulk_create.call_count == 1

    @patch('training.config.settings', 'JWT_SECRET', 'super_secret')
    @patch('training.api.api_v1.gspc.send_gspc_invite_emails')
    def test_gspc_invite_parses_valid_emails(self, gspc_admin_invite, goodJWT, standard_payload, fake_gspc_invite_repo):
        '''Given 2 valid emails in a list of 4 it should return a list of 2 valid emails'''
        response = post_gspc_invite(standard_payload, goodJWT)

        emailList = response.json()['valid_emails']
        assert len(emailList) == 2
        assert "ValidEmail@test.com" in emailList
        assert "ValidEmail2@test.com" in emailList

    @patch('training.config.settings', 'JWT_SECRET', 'super_secret')
    @patch('training.api.api_v1.gspc.send_gspc_invite_emails')
    def test_gspc_invite_parses_invalid_emails(self, gspc_admin_invite, goodJWT, standard_payload, fake_gspc_invite_repo):
        '''Given 2 invalid emails in a list of 4 it should return a list of 2 invalid emails'''
        response = post_gspc_invite(standard_payload, goodJWT)

        emailList = response.json()['invalid_emails']
        assert len(emailList) == 2
        assert "invalidEmail" in emailList
        assert "@invalidEmail.2" in emailList

    def test_gspc_report(self, goodJWT, fake_gspc_invite_repo):
        '''Given a valid request returns a csv'''
        response = post_gspc_report(goodJWT)
        assert response.status_code == HTTPStatus.OK
        assert fake_gspc_invite_repo.get_gspc_completion_report.call_count == 1

        # Assert the media type
        assert response.headers["content-type"] == "application/csv"

        # Assert the Content-Disposition header
        assert "Content-Disposition" in response.headers
        assert response.headers["Content-Disposition"] == 'attachment; filename="GspcCompletionReport.csv"'

    def test_gspc_report_no_perms(self, badJWT, fake_gspc_invite_repo):
        '''Endpoint requires admin role'''
        response = post_gspc_report(badJWT)
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @patch('training.api.api_v1.gspc.send_gspc_invite_emails')
    def test_gspc_follow_up_success(self, mock_send_emails, goodJWT, fake_gspc_invite_repo, mock_follow_up_invites):
        '''Test that follow-up emails are properly scheduled when admin makes request'''
        # Set up mock repository responses
        fake_gspc_invite_repo.get_invites_for_second_follow_up.return_value = mock_follow_up_invites["second"]
        fake_gspc_invite_repo.get_invites_for_final_follow_up.return_value = mock_follow_up_invites["final"]

        # Make request
        response = post_gspc_follow_up(goodJWT)

        # Verify response
        assert response.status_code == HTTPStatus.OK

        # Verify repository methods called
        fake_gspc_invite_repo.get_invites_for_second_follow_up.assert_called_once()
        fake_gspc_invite_repo.get_invites_for_final_follow_up.assert_called_once()

    def test_gspc_follow_up_no_perms(self, badJWT, fake_gspc_invite_repo):
        '''Test that follow-up endpoint requires admin role'''
        response = post_gspc_follow_up(badJWT)
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @patch('training.api.api_v1.gspc.send_gspc_invite_emails')
    def test_gspc_follow_up_empty_lists(self, mock_send_emails, goodJWT, fake_gspc_invite_repo):
        '''Test that follow-up works even when no emails need to be sent'''
        # Set up mock repository responses with empty lists
        fake_gspc_invite_repo.get_invites_for_second_follow_up.return_value = []
        fake_gspc_invite_repo.get_invites_for_final_follow_up.return_value = []

        # Make request
        response = post_gspc_follow_up(goodJWT)

        # Verify response is still OK
        assert response.status_code == HTTPStatus.OK

        # Verify repository methods called
        fake_gspc_invite_repo.get_invites_for_second_follow_up.assert_called_once()
        fake_gspc_invite_repo.get_invites_for_final_follow_up.assert_called_once()
