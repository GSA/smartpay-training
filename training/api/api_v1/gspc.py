from typing import List
from fastapi import APIRouter, status, HTTPException
from training.schemas.gspc_invite import GspcInvite

router = APIRouter()

#todo limit to admins 
@router.post("/gspc-invite")
async def gspc_admin_invite(
    GspcInvite: GspcInvite
):
    try:
        #Parse emails string into valid and invalid email list
        GspcInvite.parse()

        #todo Save valid emails to db

        #todo Send Email to each valid user 

        #Return object with both list for succcess and failure messages
        return GspcInvite
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid user id or agencies ids"
        )
