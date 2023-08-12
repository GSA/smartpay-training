import json
from uuid import uuid4
from typing import Optional
from redis import Redis

from training.config import settings
from training.schemas import TempUser, UserCreate


redis = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    ssl=settings.REDIS_TLS,
    ssl_cert_reqs=None,
)


class UserCache:
    '''
    Accessor methods for redis cache to create temp tokens associated
    with users.
    '''

    CACHE_TTL = settings.EMAIL_TOKEN_TTL

    def get(self, token: str) -> Optional[UserCreate]:
        user = redis.get(token)
        if user:
            user = json.loads(user)
            return UserCreate(**user)

    def set(self, user: TempUser) -> str:
        token = str(uuid4())
        user_str = user.model_dump_json()
        # try/except here
        redis.set(token, user_str)
        redis.expire(token, self.CACHE_TTL)
        return token

    def delete(self, token: str):
        redis.delete(token)
