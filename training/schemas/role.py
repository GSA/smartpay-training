from pydantic import ConfigDict, BaseModel


class RoleCreate(BaseModel):
    name: str


class Role(RoleCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
