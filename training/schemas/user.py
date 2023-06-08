from pydantic import BaseModel, EmailStr
from training.schemas.agency import Agency
from training.schemas.role import Role


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    agency_id: int
    pass


class User(UserBase):
    id: int
    agency_id: int
    roles: list[Role]
    report_agencies: list[Agency]

    class Config:
        orm_mode = True
