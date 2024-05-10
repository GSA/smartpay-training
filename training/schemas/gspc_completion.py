from typing import Any
from pydantic import BaseModel


class GspcCompletion(BaseModel):
    user_id: int
    passed: bool
    certification_expiration_date: str
    responses: dict[str, Any]
