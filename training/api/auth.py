
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
import jwt
from training.config import settings
from fastapi import Form


class JWTUser(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials | None = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            user = self.decode_jwt(credentials.credentials)
            if user is None:
                raise HTTPException(status_code=403, detail="Invalid or expired token.")
            return user
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def decode_jwt(self, token: str):
        try:
            return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        except jwt.exceptions.InvalidTokenError:
            return


class RequireRole:
    def __init__(self, required_roles: list[str]) -> None:
        self.required_roles = set(required_roles)

    def __call__(self, user=Depends(JWTUser())):
        try:
            user_roles = user['roles']
        except KeyError:
            raise HTTPException(status_code=401, detail="Not Authorized")

        if all(role in user_roles for role in self.required_roles):
            return user
        else:
            raise HTTPException(status_code=401, detail="Not Authorized")


def user_from_form(jwtToken: Annotated[str, Form()]):
    try:
        return jwt.decode(jwtToken, settings.JWT_SECRET, algorithms=["HS256"])
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Not Authorized")
