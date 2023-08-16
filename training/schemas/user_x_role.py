from pydantic import ConfigDict, BaseModel


class UserXRole(BaseModel):
    user_id: int
    role_id: int
    model_config = ConfigDict(from_attributes=True)
