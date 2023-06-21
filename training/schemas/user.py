from datetime import datetime
from pydantic import BaseModel, EmailStr, validator
from training.schemas.agency import Agency
from training.schemas.role import Role


def convert_roles(cls, input) -> list[str]:
    # Converts roles from a list of dicts to a simple list of role name strings.
    return list(map(lambda role: role.name, input))


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    agency_id: int
    pass


class User(UserBase):
    id: int
    agency_id: int
    agency: Agency
    roles: list[Role]
    report_agencies: list[Agency]

    class Config:
        orm_mode = True


class UserJWT(User):
    # Provides a user object that is appropriate for encoding into a JWT.

    roles: list[str]
    _roles_validator = validator("roles", pre=True, allow_reuse=True)(convert_roles)


class UserQuizCompletionReportData(UserBase):
    agency: str
    bureau: str | None
    quiz: str
    completion_date: datetime

    class Config:
        orm_mode = True


class UserSearchResult(BaseModel):
    users: list[User]
    total_count: int

    class Config:
        orm_mode = True
