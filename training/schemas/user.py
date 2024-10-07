from pydantic import ConfigDict, BaseModel, EmailStr, field_validator
from training.schemas.agency import Agency
from training.schemas.role import Role
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    agency_id: int
    pass


class UserUpdate(UserBase):
    agency_id: int


class User(UserBase):
    id: int
    agency_id: int
    agency: Agency
    roles: list[Role]
    report_agencies: list[Agency]
    created_on: str
    created_by: str
    modified_on: Optional[str] = None
    modified_by: Optional[str] = None

    def is_admin(self) -> bool:
        role_names = [role.name.upper() for role in self.roles]
        return "Admin".upper() in role_names

    model_config = ConfigDict(from_attributes=True)

    @field_validator('created_on', 'modified_on', mode='before')
    def convert_datetime(cls, input):
        if isinstance(input, datetime):
            return input.isoformat()
        return input


class UserJWT(User):
    # Provides a user object that is appropriate for encoding into a JWT.

    roles: list[str]

    @field_validator('roles', mode='before')
    def convert_roles(cls, input) -> list[str]:
        # Converts roles from a list of dicts to a simple list of role name strings.
        return [role.name for role in input]


class UserSearchResult(BaseModel):
    users: list[User]
    total_count: int

    @field_validator('users', mode='before')
    def convert_user_datetimes(cls, input):
        for user in input:
            if isinstance(user.created_on, datetime):
                user.created_on = user.created_on.isoformat()
            if user.modified_on and isinstance(user.modified_on, datetime):
                user.modified_on = user.modified_on.isoformat()
        return input

    model_config = ConfigDict(from_attributes=True)
