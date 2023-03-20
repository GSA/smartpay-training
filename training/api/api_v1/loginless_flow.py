import logging
import jwt

from fastapi import APIRouter, status, HTTPException, Depends
from training.schemas import TempUser
from training.data import UserCache
from training.config import settings
from training.api.email import send_email
from training.api.auth import JWTUser

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
    # http://127.0.0.1:5173?t=99e554ad-7e28-4429-914d-e725dbade3c7
    # which would hit the endpoint below

    url = f"{settings.BASE_URL}/home?t={token}"
    try:
        res = await send_email(to_email=user.email, name=user.first_name, link=url)

    except Exception as e:
        logging.error("Error sending mail", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server Error"
        )

    return {"token": url, "response": res}


@router.get("/user-info")
def user_info(user=Depends(JWTUser())):
    # This will eventually query the DB for the
    # info we want to display on a user's home page
    # But for now just send the jwt data
    return user


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
    encoded_jwt = jwt.encode(user.dict(), settings.JWT_SECRET, algorithm="HS256")

    return {'user': user, 'jwt': encoded_jwt}
