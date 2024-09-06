import pytest
import jwt


from unittest.mock import MagicMock
from fastapi import status, HTTPException
from fastapi.testclient import TestClient
from training.api.deps import certificate_repository
from training.config import settings
from training.main import app
from training.schemas import UserCertificate, GspcCertificate, CertificateListValue
from training.services.certificate import Certificate
from training.api.api_v1.certificates import verify_certificate_is_valid, is_admin

client = TestClient(app)


@pytest.fixture
def user_cert():
    return {
        'id': 1,
        'user_id': 2,
        'user_name': "Molly",
        'agency': 'Freeman Journal',
        'quiz_id': 100,
        'quiz_name': "Dublin History",
        'completion_date': '2023-08-21T22:59:36'
    }


@pytest.fixture
def gspc_cert():
    return {
        'id': 1,
        'user_id': 2,
        'user_name': "Molly",
        'agency': 'Freeman Journal',
        'completion_date': '2023-08-21T22:59:36',
        'certification_expiration_date': '2024-08-21'
    }


@pytest.fixture
def cert_list_value():
    return {
        'id': 1,
        'user_id': 2,
        'user_name': "Molly",
        'cert_title': "Dublin History",
        'completion_date': '2023-08-21T22:59:36',
        'certificate_type': 1
    }


@pytest.fixture
def admin_user():
    return {
        'name': 'Albus Dumbledore',
        'email': 'dumbledore@hogwarts.edu',
        'roles': ['Admin']
    }


@pytest.fixture
def adminJWT(admin_user):
    return jwt.encode(admin_user, settings.JWT_SECRET, algorithm="HS256")


@pytest.fixture
def fake_cert_repo():
    mock = MagicMock()
    app.dependency_overrides[certificate_repository] = lambda: mock
    yield mock
    app.dependency_overrides = {}


@pytest.fixture
def fake_cert_service_repo():
    mock = MagicMock()
    app.dependency_overrides[Certificate] = lambda: mock
    yield mock
    app.dependency_overrides = {}


@pytest.fixture
def goodJWT():
    return jwt.encode({'id': 1}, settings.JWT_SECRET, algorithm="HS256")


class MockCertificate:
    def __init__(self, user_id):
        self.user_id = user_id


class TestCertificateAPI:
    def test_get_certificates_no_auth(self, fake_cert_repo):
        response = client.get(
            "/api/v1/certificates"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_no_certificates(self, fake_cert_repo, goodJWT):
        fake_cert_repo.get_all_certificates_by_userId.return_value = None
        response = client.get(
            "/api/v1/certificates",
            headers={"Authorization": f"Bearer {goodJWT}"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_gets_certificates_by_type_and_id(self, fake_cert_repo, goodJWT):
        fake_cert_repo.get_all_certificates_by_userId.return_value = None
        client.get(
            "/api/v1/certificates",
            headers={"Authorization": f"Bearer {goodJWT}"}
        )
        fake_cert_repo.get_all_certificates_by_userId.assert_called_once_with(1)

    def test_gets_certificates(self, fake_cert_repo, goodJWT, cert_list_value):
        cert = CertificateListValue.model_validate(cert_list_value)
        fake_cert_repo.get_all_certificates_by_userId.return_value = [cert]
        response = client.get(
            "/api/v1/certificates",
            headers={"Authorization": f"Bearer {goodJWT}"}
        )
        assert response.json() == [cert_list_value]

    def test_gets_certificates_by_userId(self, fake_cert_repo, adminJWT, cert_list_value):
        cert = CertificateListValue.model_validate(cert_list_value)
        fake_cert_repo.get_all_certificates_by_userId.return_value = [cert]
        response = client.get(
            "/api/v1/certificates/2",
            headers={"Authorization": f"Bearer {adminJWT}"}
        )
        assert response.json() == [cert_list_value]

    def test_gets_certificates_by_userId_no_admin_role(self, goodJWT):
        response = client.get(
            "/api/v1/certificates/2",
            headers={"Authorization": f"Bearer {goodJWT}"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_specific_certificate_not_found(self, fake_cert_repo, goodJWT):
        fake_cert_repo.get_certificate_by_id.return_value = None
        response = client.post(
            "/api/v1/certificate/1/2",
            data={"jwtToken": goodJWT}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        fake_cert_repo.get_certificate_by_id.assert_called_once_with(2)

    def test_get_specific_certificate_wrong_user(self, fake_cert_repo, goodJWT, cert_list_value):
        cert = CertificateListValue.model_validate(cert_list_value)
        fake_cert_repo.get_certificate_by_id.return_value = cert
        response = client.post(
            "/api/v1/certificate/1/2",
            data={"jwtToken": goodJWT}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_specific_quiz_certificate(self, fake_cert_repo, goodJWT, user_cert, fake_cert_service_repo):
        user_cert['user_id'] = 1
        cert = UserCertificate.model_validate(user_cert)
        fake_cert_repo.get_certificate_by_id.return_value = cert
        fake_cert_service_repo.generate_pdf.return_value = b'some bytes'

        response = client.post(
            "/api/v1/certificate/1/2",
            data={"jwtToken": goodJWT}
        )
        fake_cert_service_repo.generate_pdf.assert_called_once_with(
            cert.quiz_name,
            cert.user_name,
            cert.agency,
            cert.completion_date
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.headers['content-type'] == 'application/pdf'
        assert response.headers['content-disposition'] == 'attachment; filename="SmartPayTraining.pdf"'
        assert response.text == "some bytes"

    def test_gets_certificates_unknown_type(self, fake_cert_repo, goodJWT):
        fake_cert_repo.get_certificates_by_userId.return_value = None
        response = client.get(
            "/api/v1/certificates/new-type",
            headers={"Authorization": f"Bearer {goodJWT}"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_specific_gspc_certificate(self, fake_cert_repo, goodJWT, gspc_cert, fake_cert_service_repo):
        gspc_cert['user_id'] = 1
        cert = GspcCertificate.model_validate(gspc_cert)
        fake_cert_repo.get_gspc_certificate_by_id.return_value = cert
        fake_cert_service_repo.generate_gspc_pdf.return_value = b'some bytes'

        response = client.post(
            "/api/v1/certificate/2/2",
            data={"jwtToken": goodJWT}
        )
        fake_cert_service_repo.generate_gspc_pdf.assert_called_once_with(
            cert.user_name,
            cert.agency,
            cert.completion_date,
            cert.certification_expiration_date
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.headers['content-type'] == 'application/pdf'
        assert response.headers['content-disposition'] == 'attachment; filename="GSA SmartPay Program Certification.pdf"'
        assert response.text == "some bytes"

    def test_get_specific_gspc_certificate_not_found(self, fake_cert_repo, goodJWT):
        fake_cert_repo.get_gspc_certificate_by_id.return_value = None
        response = client.post(
            "/api/v1/certificate/2/2",
            data={"jwtToken": goodJWT}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        fake_cert_repo.get_gspc_certificate_by_id.assert_called_once_with(2)

    def test_get_specific_gspc_certificate_wrong_user(self, fake_cert_repo, goodJWT, gspc_cert):
        cert = GspcCertificate.model_validate(gspc_cert)
        fake_cert_repo.get_gspc_certificate_by_id.return_value = cert
        response = client.post(
            "/api/v1/certificate/2/2",
            data={"jwtToken": goodJWT}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_verify_certificate_is_valid_certificate_none(self):
        """Test when the certificate is None, should raise 404 HTTPException."""
        with pytest.raises(HTTPException) as exc_info:
            verify_certificate_is_valid(cert=None, user_id=1, is_admin_user=False)
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND

    def test_verify_certificate_is_valid_user_not_authorized(self):
        """Test when user_id does not match and is not an admin, should raise 401 HTTPException."""
        cert = MockCertificate(user_id=2)
        with pytest.raises(HTTPException) as exc_info:
            verify_certificate_is_valid(cert=cert, user_id=1, is_admin_user=False)
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Not Authorized"

    def test_verify_certificate_is_valid_user_authorized(self):
        """Test when user_id matches, should not raise any exception."""
        cert = MockCertificate(user_id=1)
        try:
            verify_certificate_is_valid(cert=cert, user_id=1, is_admin_user=False)
        except HTTPException:
            pytest.fail("HTTPException raised unexpectedly!")

    def test_verify_certificate_is_valid_admin_user(self):
        """Test when the user is an admin, should not raise any exception even if user_id does not match."""
        cert = MockCertificate(user_id=2)
        try:
            verify_certificate_is_valid(cert=cert, user_id=1, is_admin_user=True)
        except HTTPException:
            pytest.fail("HTTPException raised unexpectedly!")

    def test_is_admin_with_admin_role(self):
        """Test when 'Admin' is in the roles list."""
        user = {"roles": ["User", "Admin", "Editor"]}
        assert is_admin(user) is True

    def test_is_admin_without_admin_role(self):
        """Test when 'Admin' is not in the roles list."""
        user = {"roles": ["User", "Editor"]}
        assert is_admin(user) is False

    def test_is_admin_empty_roles(self):
        """Test when the roles list is empty."""
        user = {"roles": []}
        assert is_admin(user) is False

    def test_is_admin_roles_is_none(self):
        """Test when the roles list is None."""
        user = {"roles": None}
        assert is_admin(user) is False

    def test_is_admin_roles_key_missing(self):
        """Test when the roles key is missing from the dictionary."""
        user = {}
        assert is_admin(user) is False
