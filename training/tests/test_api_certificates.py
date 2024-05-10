import pytest
import jwt


from unittest.mock import MagicMock
from fastapi import status
from fastapi.testclient import TestClient
from training.api.deps import certificate_repository
from training.config import settings
from training.main import app
from training.schemas import UserCertificate, GspcCertificate
from training.services.certificate import Certificate

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


class TestCertificateAPI:
    def test_get_certificates_no_auth(self, fake_cert_repo):
        response = client.get(
            "/api/v1/certificates"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_no_certificates(self, fake_cert_repo, goodJWT):
        fake_cert_repo.get_certificates_by_userid.return_value = None
        response = client.get(
            "/api/v1/certificates",
            headers={"Authorization": f"Bearer {goodJWT}"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_gets_certificates_by_type_and_id(self, fake_cert_repo, goodJWT):
        fake_cert_repo.get_certificates_by_userid.return_value = None
        client.get(
            "/api/v1/certificates",
            headers={"Authorization": f"Bearer {goodJWT}"}
        )
        fake_cert_repo.get_certificates_by_userid.assert_called_once_with(1)

    def test_gets_certificates(self, fake_cert_repo, goodJWT, user_cert):
        cert = UserCertificate.model_validate(user_cert)
        fake_cert_repo.get_certificates_by_userid.return_value = [cert]
        response = client.get(
            "/api/v1/certificates",
            headers={"Authorization": f"Bearer {goodJWT}"}
        )
        assert response.json() == [user_cert]

    def test_get_specific_certificate_not_found(self, fake_cert_repo, goodJWT):
        fake_cert_repo.get_certificate_by_id.return_value = None
        response = client.post(
            "/api/v1/certificate/quiz/2",
            data={"jwtToken": goodJWT}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        fake_cert_repo.get_certificate_by_id.assert_called_once_with(2)

    def test_get_specific_certificate_wrong_user(self, fake_cert_repo, goodJWT, user_cert):
        cert = UserCertificate.model_validate(user_cert)
        fake_cert_repo.get_certificate_by_id.return_value = cert
        response = client.post(
            "/api/v1/certificate/quiz/2",
            data={"jwtToken": goodJWT}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_specific_quiz_certificate(self, fake_cert_repo, goodJWT, user_cert, fake_cert_service_repo):
        user_cert['user_id'] = 1
        cert = UserCertificate.model_validate(user_cert)
        fake_cert_repo.get_certificate_by_id.return_value = cert
        fake_cert_service_repo.generate_pdf.return_value = b'some bytes'

        response = client.post(
            "/api/v1/certificate/quiz/2",
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
        fake_cert_repo.get_certificates_by_userid.return_value = None
        response = client.get(
            "/api/v1/certificates/new-type",
            headers={"Authorization": f"Bearer {goodJWT}"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_specific_gspc_certificate(self, fake_cert_repo, goodJWT, gspc_cert, fake_cert_service_repo):
        gspc_cert['user_id'] = 1
        cert = GspcCertificate.model_validate(gspc_cert)
        fake_cert_repo.get_gspc_certificate_by_id.return_value = cert
        fake_cert_service_repo.generate_gspc_pdf.return_value = b'some bytes'

        response = client.post(
            "/api/v1/certificate/gspc/2",
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
        assert response.headers['content-disposition'] == 'attachment; filename="GSPC Certification.pdf"'
        assert response.text == "some bytes"

    def test_get_specific_gspc_certificate_not_found(self, fake_cert_repo, goodJWT):
        fake_cert_repo.get_gspc_certificate_by_id.return_value = None
        response = client.post(
            "/api/v1/certificate/gspc/2",
            data={"jwtToken": goodJWT}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        fake_cert_repo.get_gspc_certificate_by_id.assert_called_once_with(2)

    def test_get_specific_gspc_certificate_wrong_user(self, fake_cert_repo, goodJWT, gspc_cert):
        cert = GspcCertificate.model_validate(gspc_cert)
        fake_cert_repo.get_gspc_certificate_by_id.return_value = cert
        response = client.post(
            "/api/v1/certificate/gspc/2",
            data={"jwtToken": goodJWT}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
