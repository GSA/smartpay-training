from datetime import datetime
from pydantic import BaseModel


class UserCertificate(BaseModel):
    user_id: int
    user_name: str
    quiz_id: int
    quiz_name: str
    completion_date: datetime

    class Config:
        orm_mode = True
