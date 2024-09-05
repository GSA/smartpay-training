from typing import List, Any, Dict
from fastapi import APIRouter, status, HTTPException, Depends, Response
from training.schemas import UserCertificate, CertificateType, CertificateListValue
from training.repositories import CertificateRepository
from training.api.deps import certificate_repository
from training.services.certificate import Certificate
from training.api.auth import JWTUser, user_from_form
from training.api.auth import RequireRole


router = APIRouter()


@router.get("/certificates/{userId}", response_model=List[CertificateListValue])
def get_certificates_by_userId(
    userId: int,
    user=Depends(RequireRole(["Admin"])),
    repo: CertificateRepository = Depends(certificate_repository),
):
    '''
    Returns a list of certificates for `userId`
    '''
    db_user_certificates = repo.get_all_certificates_by_userId(userId)

    if db_user_certificates is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_user_certificates


@router.get("/certificates/", response_model=List[CertificateListValue])
def get_certificates_by_user(
    repo: CertificateRepository = Depends(certificate_repository),
    user: dict[str, Any] = Depends(JWTUser())
):
    '''
    Returns a list of certificates for current `user`
    '''
    db_user_certificates = repo.get_all_certificates_by_userId(user["id"])

    if db_user_certificates is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_user_certificates


@router.post("/certificate/{certType}/{id}", response_model=UserCertificate)
def get_certificate_by_type_and_id(
        id: int,
        certType: int,
        certificateRepo: CertificateRepository = Depends(certificate_repository),
        certificateService: Certificate = Depends(Certificate),
        user=Depends(user_from_form)
):
    pdf_bytes = None
    filename = ''
    is_admin_user = is_admin(user)
    user_id = user["id"]

    if (certType == CertificateType.QUIZ.value):
        db_user_certificate = certificateRepo.get_certificate_by_id(id)

        verify_certificate_is_valid(db_user_certificate, user_id, is_admin_user)

        pdf_bytes = certificateService.generate_pdf(
            db_user_certificate.quiz_name,
            db_user_certificate.user_name,
            db_user_certificate.agency,
            db_user_certificate.completion_date
        )

        filename = "SmartPayTraining.pdf"
    elif (certType == CertificateType.GSPC.value):
        certificate = certificateRepo.get_gspc_certificate_by_id(id)

        verify_certificate_is_valid(certificate, user_id, is_admin_user)

        pdf_bytes = certificateService.generate_gspc_pdf(
            certificate.user_name,
            certificate.agency,
            certificate.completion_date,
            certificate.certification_expiration_date
        )

        filename = "GSA SmartPay Program Certification.pdf"
    else:
        # type not implemented
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
    return Response(pdf_bytes, headers=headers, media_type='application/pdf')


def verify_certificate_is_valid(cert: object, user_id: int, is_admin_user: bool):
    if cert is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if cert.user_id != user_id and not is_admin_user:
        raise HTTPException(status_code=401, detail="Not Authorized")


def is_admin(user: Dict[str, List[str]]) -> bool:
    # Ensure that 'roles' is in the user dictionary and is a list
    if 'roles' not in user or not isinstance(user['roles'], list):
        return False

    # Normalize roles to avoid case sensitivity issues
    return 'Admin' in user['roles']
