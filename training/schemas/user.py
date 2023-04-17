from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    agency_id: int
    pass


class User(UserBase):
    id: int
    agency_id: int

    class Config:
        orm_mode = True


class UserCertificate(BaseModel):
    user_id: int
    user_name: str
    quiz_id: int
    quiz_name: str
    completion_date: datetime

    class Config:
        orm_mode = True
