from typing import List
import logging
from fastapi import APIRouter, status, HTTPException, Depends
from training.schemas.gspc_invite import GspcInvite
from training.repositories import GspcInviteRepository
from training.api.deps import gspc_invite_repository
from training.api.email import send_gspc_invite_email

router = APIRouter()

#todo limit to admins 
#todo tests
#todo documentation
@router.post("/gspc-invite")
async def gspc_admin_invite(
    GspcInvite: GspcInvite,
    repo: GspcInviteRepository = Depends(gspc_invite_repository)
):
    try:
        #Parse emails string into valid and invalid email list
        GspcInvite.parse()

        for email in GspcInvite.valid_emails:
            repo.create(email = email, certification_expiration_date = GspcInvite.certification_expiration_date)

        #todo multithreading            
        for email in GspcInvite.valid_emails:
            try:
                send_gspc_invite_email(to_email=email)
                logging.info(f"Sent gspc invite email to {email}")
            except Exception as e:
                logging.error("Error sending gspc invite email", e)

        #Return object with both list for succcess and failure messages
        return GspcInvite
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="emails or experation date"
        )
