
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

