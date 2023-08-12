import logging
import jwt
from typing import Union

from fastapi import APIRouter, status, Response, HTTPException, Depends, Request
from training.schemas import TempUser, IncompleteTempUser, WebDestination, UserJWT
from training.data import UserCache
from training.repositories import UserRepository
from training.api.deps import user_repository

from training.config import settings
from training.api.email import send_email
from training.api.auth import JWTUser

router = APIRouter()


# This lookup table allows the front-end to send a simple pageID
# but be redirected to a more complex path. It also allows the
# backend to provide errors if the user does not have the appropriate
# role for a front-end page (although the data itself is secured by the API)
def page_lookup():
    return {
        'certificates': {'path': '/certificates/', 'required_roles': []},
        'training_reports': {'path': '/training_reports', 'required_roles': ['Report']},
        'training_travel': {'path': '/quiz/training_travel/', 'required_roles': []},
        'training_purchase': {'path': '/quiz/training_purchase/', 'required_roles': []},
        'training_travel_pc': {'path': '/quiz/training_travel_pc/', 'required_roles': []},
        'training_purchase_pc': {'path': '/quiz/training_purchase_pc/', 'required_roles': []},
        'training_fleet_pc': {'path': '/quiz/training_fleet_pc/', 'required_roles': []},
    }


@router.post("/get-link", status_code=status.HTTP_201_CREATED)
async def send_link(
    response: Response,
    request: Request,
    user: Union[TempUser, IncompleteTempUser],
    dest: WebDestination,
    repo: UserRepository = Depends(user_repository),
    cache: UserCache = Depends(UserCache),
    page_id_lookup: dict = Depends(page_lookup)
):
    tu = await request.json()
    print("res: ", tu)
    print("user: ", type(user))
    try:
        required_roles = page_id_lookup[dest.page_id]['required_roles']
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unkown Page Id {dest.page_id}"
        )
    if isinstance(user, IncompleteTempUser):
        user_from_db = repo.find_by_email(user.email)
        if user_from_db is None:
            response.status_code = status.HTTP_200_OK
            return {'new': True}
        else:
            role_names = set(role.name for role in user_from_db.roles)
            if not all(role in role_names for role in required_roles):
                logging.info(
                    f"{user.email} does not have the required role to access {page_id_lookup[dest.page_id]['path']}"
                )
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unauthorized"
                )

            user = TempUser.model_validate({
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
    path = page_id_lookup[dest.page_id]['path']
    url = f"{settings.BASE_URL}{path}?t={token}"
    try:
        send_email(to_email=user.email, name=user.name, link=url, training_title=dest.title)
        logging.info(f"Sent confirmation email to {user.email} for {path}")
    except Exception as e:
        logging.error("Error sending mail", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server Error"
        )


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
    user_return = UserJWT.model_validate(db_user)
    logging.info(f"Confirmed email token for {user.email}")
    encoded_jwt = jwt.encode(user_return.model_dump(), settings.JWT_SECRET, algorithm="HS256")
    return {'user': user_return, 'jwt': encoded_jwt}
