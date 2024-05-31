from typing import Any
import logging
import csv
from io import StringIO
from fastapi import APIRouter, status, HTTPException, Response, Depends
from training.schemas import GspcInvite, GspcResult, GspcSubmission
from training.services import GspcService
from training.repositories import GspcInviteRepository, GspcCompletionRepository
from training.api.deps import gspc_invite_repository, gspc_completion_repository, gspc_service
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


@router.post("/gspc/download-gspc-completion-report")
def download_report_csv(
        user=Depends(RequireRole(["Admin"])),
        gspc_completion_repo: GspcCompletionRepository = Depends(gspc_completion_repository),
):
    results = gspc_completion_repo.get_gspc_completion_report()

    output = StringIO()
    writer = csv.writer(output)

    # header row
    writer.writerow(['Invited Email', 'Registered Email', 'Name', 'Agency', 'Bureau', 'Passed', 'Registration Completion Date and Time'])
    for item in results:
        # data row
        completion_date_str = item.completionDate.strftime("%m/%d/%Y %H:%M:%S") if item.completionDate is not None else None
        writer.writerow([item.invitedEmail, item.registeredEmail, item.username ,item.agency, item.bureau, item.passed, completion_date_str])  # noqa 501

    headers = {'Content-Disposition': 'attachment; filename="GspcCompletionReport.csv"'}
    return Response(output.getvalue(), headers=headers, media_type='application/csv')
