from typing import Any
import csv
from io import StringIO
from fastapi import APIRouter, status, HTTPException, Response, Depends
from training.schemas import GspcInvite, GspcResult, GspcSubmission
from training.services import GspcService
from training.repositories import GspcInviteRepository
from training.api.deps import gspc_invite_repository, gspc_service
from training.api.email import GspcEmailVersion, InviteTuple, send_gspc_invite_emails
from training.api.auth import RequireRole
from training.api.auth import JWTUser
from fastapi import BackgroundTasks
from training.config import settings


router = APIRouter()


@router.post("/gspc/send-invites")
async def gspc_admin_invite(
    gspcInvite: GspcInvite,
    background_tasks: BackgroundTasks,
    repo: GspcInviteRepository = Depends(gspc_invite_repository),
    user=Depends(RequireRole(["Admin"]))
):
    '''
    Given a list of emails we parse them into two list (valid and invalid).
    Then we log each of the valid emails to the db and shoot off an email to each.
    '''
    try:
        # Parse emails string into valid and invalid email list
        gspcInvite.parse()

        entities = repo.bulk_create(emails=gspcInvite.valid_emails, certification_expiration_date=gspcInvite.certification_expiration_date)

        # Explicitly load needed props into memory before passing to the background task
        entities_data = [InviteTuple(entity.gspc_invite_id, entity.email, GspcEmailVersion.INITIAL) for entity in entities]

        # Add email sending to background tasks
        # note: passing in settings as the background task looses the current app context once triggered
        background_tasks.add_task(send_gspc_invite_emails, invites=entities_data, app_settings=settings)

        # Return object with both list for success and failure messages
        return gspcInvite
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="emails or expiration date"
        )


@router.post("/gspc/send-follow-ups")
async def gspc_admin_invite_follow_up(
    background_tasks: BackgroundTasks,
    repo: GspcInviteRepository = Depends(gspc_invite_repository),
    user=Depends(RequireRole(["Admin"]))
):
    '''
    Fetches GSPC admin invites that require second and final follow-up emails and schedules them for sending as a background task.
    '''
    # Explicitly load needed props into memory before passing to the background task
    second_follow_up_emails = repo.get_invites_for_second_follow_up()
    second_entities_data = [InviteTuple(entity.gspc_invite_id, entity.email, GspcEmailVersion.SECOND) for entity in second_follow_up_emails]

    final_follow_up_emails = repo.get_invites_for_final_follow_up()
    final_entities_data = [InviteTuple(entity.gspc_invite_id, entity.email, GspcEmailVersion.FINAL) for entity in final_follow_up_emails]

    # Concatenate both lists
    combined_entities_data = second_entities_data + final_entities_data

    # Add email sending to background tasks
    # note: passing in settings as the background task looses the current app context once triggered
    background_tasks.add_task(send_gspc_invite_emails, invites=combined_entities_data, app_settings=settings)

    return Response(status_code=status.HTTP_200_OK)


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
        repo: GspcInviteRepository = Depends(gspc_invite_repository),
):
    results = repo.get_gspc_completion_report()

    output = StringIO()
    writer = csv.writer(output)

    # header row
    writer.writerow(['Invited Email', 'Unique Identifier', 'Invitation Sent Date and Time',
                     'Follow-up Email Sent Date and Time', 'Final Email Sent Date and Time',
                     'Registered Email', 'Name',
                     'Agency', 'Bureau',
                     'Passed', 'Registration Completion Date and Time'])

    dateStrFormat = "%m/%d/%Y %H:%M:%S"
    for item in results:
        # format datetime values
        completion_date_str = item.completedDate.strftime(dateStrFormat) if item.completedDate is not None else None
        invite_date_str = item.inviteDate.strftime(dateStrFormat) if item.inviteDate is not None else None
        second_invite_date_str = item.secondInviteDate.strftime(dateStrFormat) if item.secondInviteDate is not None else None
        final_invite_date_str = item.finalInviteDate.strftime(dateStrFormat) if item.finalInviteDate is not None else None

        writer.writerow([item.invitedEmail, item.gspcInviteId, invite_date_str, second_invite_date_str, final_invite_date_str, item.registeredEmail, item.username ,item.agency, item.bureau, item.passed, completion_date_str])  # noqa 501

    headers = {'Content-Disposition': 'attachment; filename="GspcCompletionReport.csv"'}
    return Response(output.getvalue(), headers=headers, media_type='application/csv')
