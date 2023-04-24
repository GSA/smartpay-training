from typing import List
from fastapi import APIRouter, status, HTTPException, Depends, Response
from training.schemas import UserCertificate
from training.repositories import CertificateRepository
from training.api.deps import certificate_repository
from training.services.certificate import Certificate

router = APIRouter()


@router.get("/certificates/{user_id}", response_model=List[UserCertificate])
def get_certificates_by_userid(user_id: int, repo: CertificateRepository = Depends(certificate_repository)):
    db_user_certificates = repo.get_certificates_by_userid(user_id)
    if db_user_certificates is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_user_certificates


@router.get("/certificate/{id}", response_model=UserCertificate)
def get_certificate_by_id(
    id: int,
    repo: CertificateRepository = Depends(certificate_repository),
    certificate: Certificate = Depends(Certificate)
):

    db_user_certificate = repo.get_certificate_by_id(id)
    if db_user_certificate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    pdf_bytes = certificate.generate_pdf(
        db_user_certificate.quiz_name,
        db_user_certificate.user_name,
        db_user_certificate.completion_date
    )
    headers = {'Content-Disposition': 'attachment; filename="SmartPayTraining.pdf"'}
    return Response(pdf_bytes, headers=headers, media_type='application/pdf')
