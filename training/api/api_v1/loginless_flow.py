import logging
from fastapi import APIRouter, status, HTTPException
from training.models import TempUser
from training.data import UserCache

router = APIRouter()
u = UserCache()


@router.post("/get-link")
async def send_link(user: TempUser, status_code=status.HTTP_201_CREATED):
    try:
        token = u.set(user)
    except Exception as e:
        logging.error("Error saving user to Redis", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server Error"
        )

    # the token is the temp key in the Redis Cache
    # this it what will be needed to creat an email link such as
    # http://localhost:8000/api/v1/get-user/b8a8bb0d-a9af-4e1b-b813-b230b018363f
    # which would hit the endpoint below

    return {"token": token}


@router.get("/get-user/{token}")
async def get_user(token: str):
    try:
        user = u.get(token)
    except Exception as e:
        logging.error("Error reading token from Redis", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server Error"
        )

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return user
    # what next? redirect? Set JWT?
