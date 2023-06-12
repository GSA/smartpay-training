from pydantic import BaseModel


class UserXRole(BaseModel):
    user_id: int
    role_id: int

    class Config:
        orm_mode = True
