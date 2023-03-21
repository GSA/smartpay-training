
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from training.config import settings


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
