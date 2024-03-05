import logging
from fastapi import APIRouter, status, HTTPException, Depends
from training.schemas.gspc_invite import GspcInvite
from training.repositories import GspcInviteRepository
from training.api.deps import gspc_invite_repository
from training.api.email import send_gspc_invite_email
from training.api.auth import RequireRole

router = APIRouter()

#todo limit to admins 
#todo documentation
@router.post("/gspc-invite")
async def gspc_admin_invite(
    gspcInvite: GspcInvite,
    repo: GspcInviteRepository = Depends(gspc_invite_repository),
    user=Depends(RequireRole(["Admin"]))
):
    try:
        #Parse emails string into valid and invalid email list
        gspcInvite.parse()

        for email in gspcInvite.valid_emails:
            repo.create(email = email, certification_expiration_date = gspcInvite.certification_expiration_date)
            #If performance becomes an issue use multithreading to send the emails 
            try:
                send_gspc_invite_email(to_email=email, link="TBD")
                logging.info(f"Sent gspc invite email to {email}")
            except Exception as e:
                logging.error("Error sending gspc invite email", e)

        #Return object with both list for succcess and failure messages
        return gspcInvite
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="emails or experation date"
        )
