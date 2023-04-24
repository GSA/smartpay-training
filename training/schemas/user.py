from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    agency_id: int
    pass


class User(UserBase):
    id: int
    agency_id: int

    class Config:
        orm_mode = True
