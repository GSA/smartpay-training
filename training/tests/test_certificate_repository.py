from typing import List
from training.repositories import CertificateRepository


def test_get_certificates_by_userid(cert_repo_with_data: CertificateRepository, valid_user_ids: List[int]):

    user_id = valid_user_ids[-1]
    result = cert_repo_with_data.get_certificates_by_userid(user_id)
    assert result is not None
    assert len(result) == 1


def test_get_certificate_by_id(cert_repo_with_data: CertificateRepository, passed_quiz_completion_id):

    id = passed_quiz_completion_id
    result = cert_repo_with_data.get_certificate_by_id(id)
    assert result is not None
    assert result.id == passed_quiz_completion_id
