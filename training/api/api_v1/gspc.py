from typing import Any
import logging
from fastapi import APIRouter, status, HTTPException, Depends
from training.schemas import GspcInvite, GspcResult, GspcSubmission
from training.services import GspcService
from training.repositories import GspcInviteRepository
from training.api.deps import gspc_invite_repository, gspc_service
from training.api.email import send_gspc_invite_email
from training.api.auth import RequireRole
from training.config import settings
from training.api.auth import JWTUser


router = APIRouter()


@router.post("/gspc-invite")
async def gspc_admin_invite(
    gspcInvite: GspcInvite,
    repo: GspcInviteRepository = Depends(gspc_invite_repository),
    user=Depends(RequireRole(["Admin"]))
):
    '''
    Given a list of emails we parse them into two list (valid and invalid).
    Then we log each of the valid emails to the db and shoot of an email to each.
    '''
    try:
        # Parse emails string into valid and invalid email list
        gspcInvite.parse()

        for email in gspcInvite.valid_emails:
            repo.create(email=email, certification_expiration_date=gspcInvite.certification_expiration_date)
            # If performance becomes an issue use multithreading to send the emails
            try:
                params = gspcInvite.certification_expiration_date.strftime('%Y-%m-%d')
                link = f"{settings.BASE_URL}/gspc_registration?expirationDate={params}"
                send_gspc_invite_email(to_email=email, link=link)
                logging.info(f"Sent gspc invite email to {email}")
            except Exception as e:
                logging.error("Error sending gspc invite email", e)

        # Return object with both list for success and failure messages
        return gspcInvite
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="emails or expiration date"
        )


@router.post(
    "/gspc/submission",
    response_model=GspcResult,
    status_code=status.HTTP_201_CREATED
)
def submit_gspc_registration(
    submission: GspcSubmission,
    gspc_service: GspcService = Depends(gspc_service),
    user: dict[str, Any] = Depends(JWTUser())
):
    result = gspc_service.grade(user_id=user["id"], submission=submission)
    return result