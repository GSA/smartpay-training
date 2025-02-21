import logging
from fastapi import APIRouter, Depends, HTTPException, status
import jwt
from training.api.auth import UAAJWTUser
from training.config import settings
from training.repositories import UserRepository
from training.schemas import UserJWT, User
from training.api.deps import user_repository


router = APIRouter()


@router.get("/auth/metadata")
def auth_metadata():
    return {
        'authority': settings.AUTH_AUTHORITY_URL,
        'client_id': settings.AUTH_CLIENT_ID
    }


@router.post("/auth/exchange")
def auth_exchange(
    uaa_user=Depends(UAAJWTUser()),
    user_repo: UserRepository = Depends(user_repository),
):
    db_user = user_repo.find_by_email(uaa_user.get("email"))
    if not db_user:
        logging.info("UAA authenticated, but not found in database", extra={'user': uaa_user['email']})
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid user."
        )

    user = User.model_validate(db_user)
    if not user.is_admin():
        logging.info("UAA authenticated, but not an admin", extra={'user': uaa_user['email']})
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to login."
        )

    jwt_user = UserJWT.model_validate(db_user)
    encoded_jwt = jwt.encode(jwt_user.model_dump(), settings.JWT_SECRET, algorithm="HS256")
    logging.info("Token exchange success", extra={'user': db_user.email})
    return {'user': jwt_user, 'jwt': encoded_jwt}
