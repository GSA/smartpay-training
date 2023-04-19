from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from training.schemas import UserCertificate, QuizCompletion
from training.repositories import CertificateRepository
from training.api.deps import certificate_repository


router = APIRouter()


@router.get("/certificates/{user_id}", response_model=List[UserCertificate])
def get_certificates_by_userid(user_id: int, repo: CertificateRepository = Depends(certificate_repository)):
    db_user_certificates = repo.get_certificates_by_userid(user_id)
    if db_user_certificates is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_user_certificates


@router.get("/certificate/{id}", response_model=QuizCompletion)
def get_certificate_by_id(id: int, repo: CertificateRepository = Depends(certificate_repository)):
    db_user_certificate = repo.get_certificate_by_id(id)
    if db_user_certificate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_user_certificate
