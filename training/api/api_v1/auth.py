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
        # TODO: Log token exchange failure
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user."
        )

    user = User.from_orm(db_user)
    if not user.is_admin():
        # TODO: Log failure
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to login."
        )

    jwt_user = UserJWT.from_orm(db_user)
    encoded_jwt = jwt.encode(jwt_user.dict(), settings.JWT_SECRET, algorithm="HS256")
    # TODO: Log token exchange success
    return {'user': jwt_user, 'jwt': encoded_jwt}
