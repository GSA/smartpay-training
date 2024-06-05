from pydantic import ConfigDict, BaseModel, EmailStr, field_validator
from training.schemas.agency import Agency
from training.schemas.role import Role


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

    def is_admin(self) -> bool:
        role_names = [role.name.upper() for role in self.roles]
        return "Admin".upper() in role_names

    model_config = ConfigDict(from_attributes=True)


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
    model_config = ConfigDict(from_attributes=True)
