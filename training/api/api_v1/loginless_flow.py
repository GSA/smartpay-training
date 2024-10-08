import logging
import jwt
from typing import Union

from fastapi import APIRouter, status, Response, HTTPException, Depends
from training.schemas import TempUser, IncompleteTempUser, WebDestination, UserJWT
from training.data import UserCache
from training.repositories import UserRepository
from training.api.deps import user_repository

from training.config import settings
from training.api.email import send_email

router = APIRouter()


def page_lookup():
    '''
    Returns a lookup table to allow the front-end to send a simple pageID
    but be redirected to a more complex path. It also allows the
    backend to provide errors if the user does not have the appropriate
    role for a front-end page (although the data itself is secured by the API)
    '''
    return {
        'certificates': {'path': '/certificates/', 'required_roles': []},
        'training_reports': {'path': '/training_reports/', 'required_roles': ['Report']},
        'training_travel': {'path': '/quiz/training_travel/', 'required_roles': []},
        'training_purchase': {'path': '/quiz/training_purchase/', 'required_roles': []},
        'training_travel_pc': {'path': '/quiz/training_travel_pc/', 'required_roles': []},
        'training_purchase_pc': {'path': '/quiz/training_purchase_pc/', 'required_roles': []},
        'training_fleet_pc': {'path': '/quiz/training_fleet_pc/', 'required_roles': []},
        'gspc_registration': {'path': '/gspc_registration/', 'required_roles': []},
    }


@router.post("/get-link",
             status_code=status.HTTP_201_CREATED,
             responses={
                 200: {"description": 'OK, but user details needed'},
                 201: {"description": "Token created"}
                 })
def send_link(
    response: Response,
    user: Union[TempUser, IncompleteTempUser],
    dest: WebDestination,
    repo: UserRepository = Depends(user_repository),
    cache: UserCache = Depends(UserCache),
    page_id_lookup: dict = Depends(page_lookup)
):
    '''
    Create a link with an embedded token.\f

    This link is sent via email pointing back to the frontend section the user
    made the request from (the 'dest' parameter). The token is a key to the Redis
    cache. When they use the link to return, we have confidence they could access
    the email and look up their identity from the cache. In cases where we add the
    user to the cache this responds with an HTTP 201.

    If the `user` body parameter is an IncompleteTempUser (only has an email)
    this will query the database to see if the user exist. If the user does not exist
    this should return an HTTP 200 to indicate to the frontend that no user was created
    and it should ask them for more information (name, agency). If the email does exist,
    we send that email a link.

    A TempUser (has name, agency, and email) indicates a new user. We add this information
    to the cache and send a link, but not the database until they have validated the email.

    Parameters needed for the generated link can be passed in through the WebDestination
    object and will concatenated with the user token and added to the link.
    '''
    try:
        required_roles = page_id_lookup[dest.page_id]['required_roles']
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown Page Id {dest.page_id}"
        )
    if isinstance(user, IncompleteTempUser):
        # we only got the email from the front end
        user_from_db = repo.find_by_email(user.email)
        if user_from_db is None:
            response.status_code = status.HTTP_200_OK
            return {'new': True}
        else:
            role_names = set(role.name for role in user_from_db.roles)
            # Check to make sure the user has permission to access the destination.
            # This allows the front end to tell the user they are not authorized
            # to access this destination instead of finding out after they get the email
            # and try the link.
            if not all(role in role_names for role in required_roles):
                logging.info(
                    "unauthorized access attempt",
                    extra={'user': user.email, 'path': page_id_lookup[dest.page_id]['path']}
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
    parameters = f"t={token}" if not dest.parameters else f"{dest.parameters}&t={token}"
    url = f"{settings.BASE_URL}{path}?{parameters}"
    try:
        send_email(to_email=user.email, name=user.name, link=url, training_title=dest.title)
        logging.info("Sent confirmation email", extra={'user': user.email, 'path': path})
    except Exception as e:
        logging.error("Error sending mail", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server Error"
        )


@router.get("/get-user/{token}")
async def get_user(
    token: str,
    repo: UserRepository = Depends(user_repository),
    cache: UserCache = Depends(UserCache)
):
    '''
    Looks up the token in the redis cache to get a user who clicked a link with
    a token. If the user is not yet in the database (a new registration), create
    the user in the DB. Send back a user object with a JWT that the front end
    can use to authenticate.
    '''
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
    logging.info("Confirmed email token", extra={'user': user.email})
    encoded_jwt = jwt.encode(user_return.model_dump(), settings.JWT_SECRET, algorithm="HS256")
    return {'user': user_return, 'jwt': encoded_jwt}
