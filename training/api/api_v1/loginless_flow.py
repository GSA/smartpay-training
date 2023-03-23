import logging
import jwt
from typing import Union

from fastapi import APIRouter, status, Response, HTTPException, Depends
from training.schemas import TempUser, IncompleteTempUser
from training.data import UserCache
from training.config import settings
from training.api.email import send_email
from training.api.auth import JWTUser

router = APIRouter()
u = UserCache()


@router.post("/get-link", status_code=status.HTTP_201_CREATED)
async def send_link(user: Union[TempUser, IncompleteTempUser], response: Response):
    if isinstance(user, IncompleteTempUser):
        user_from_database = None  # replace with function to get user from email address
        if user_from_database is None:
            response.status_code = status.HTTP_200_OK
            return {'new': True}
        else:
            # here we would have these values from the DB
            # so we could make the appropriate type.
            user = TempUser.parse_obj({
                "name": "Mark Meyer",
                "email": 'mark.meyer@gsa.gov',
                "agency": "GSA",
                "page_id": user.page_id
            })
        # if we did get a user from the DB or we got a full TempUser
        # from the request, go ahead and send the link:
    try:
        token = u.set(user)
    except Exception as e:
        logging.error("Error saving user to Redis", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server Error"
        )

    # If the request is only an email, look it up in the database to see
    # if we know this user already. If not return an indication to let
    # the front-end know we need more data.
    # If we do know the user or the request has name and agency,
    # put it in the cache and send the link

    # the token is the temp key in the Redis Cache
    # this it what will be needed to creat an email link such as
    # http://127.0.0.1:5173?t=99e554ad-7e28-4429-914d-e725dbade3c7
    # which would hit the endpoint below

    url = f"{settings.BASE_URL}/quiz/{user.page_id}/?t={token}"
    try:
        res = await send_email(to_email=user.email, name=user.name, link=url)

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
