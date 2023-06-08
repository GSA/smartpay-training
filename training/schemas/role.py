from pydantic import BaseModel


class RoleCreate(BaseModel):
    name: str


class Role(RoleCreate):
    id: int

    class Config:
        orm_mode = True
