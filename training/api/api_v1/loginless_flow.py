import logging
import jwt
from typing import Union

from fastapi import APIRouter, status, Response, HTTPException, Depends
from training.schemas import TempUser, IncompleteTempUser, WebDestination, User
from training.data import UserCache
from training.repositories import UserRepository
from training.api.deps import user_repository

from training.config import settings
from training.api.email import send_email
from training.api.auth import JWTUser

router = APIRouter()


@router.post("/get-link", status_code=status.HTTP_201_CREATED)
async def send_link(
    response: Response,
    user: Union[TempUser, IncompleteTempUser],
    dest: WebDestination,
    repo: UserRepository = Depends(user_repository),
    cache: UserCache = Depends(UserCache)
):
    if isinstance(user, IncompleteTempUser):
        user_from_db = repo.find_by_email(user.email)

        if user_from_db is None:
            response.status_code = status.HTTP_200_OK
            return {'new': True}
        else:
            user = TempUser.parse_obj({
                "name": user_from_db.name,
                "email": user_from_db.email,
                "agency_id": user_from_db.agency_id,
            })
    try:
        token = cache.set(user)
    except Exception as e:
        logging.error("Error saving user to Redis", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server Error"
        )
    # TODO: make a lookup that translates page_id to a url
    # we may have the users going to pages other than quizes
    url = f"{settings.BASE_URL}/quiz/{dest.page_id}/?t={token}"
    try:
        res = await send_email(to_email=user.email, name=user.name, link=url, training_title=dest.title)
    except Exception as e:
        logging.error("Error sending mail", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server Error"
        )
    # TODO: don't send the token once we can send email
    return {"token": url, "response": res}


@router.get("/user-info")
def user_info(user=Depends(JWTUser())):
    # This will eventually query the DB for the
    # info we want to display on a user's home page
    # But for now just send the jwt data
    return user


@router.get("/get-user/{token}")
async def get_user(
    token: str,
    repo: UserRepository = Depends(user_repository),
    cache: UserCache = Depends(UserCache)
):
    try:
        user = cache.get(token)
    except Exception as e:
        logging.error("Error reading token from Redis", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server Error"
        )

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    db_user = repo.find_by_email(user.email)
    if not db_user:
        db_user = repo.create(user)
    user_return = User.from_orm(db_user)
    encoded_jwt = jwt.encode(user_return.dict(), settings.JWT_SECRET, algorithm="HS256")
    return {'user': user_return, 'jwt': encoded_jwt}
