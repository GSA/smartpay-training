from pydantic import BaseModel


class AgencyBase(BaseModel):
    name: str


class AgencyCreate(AgencyBase):
    pass


class Agency(AgencyBase):
    id: int

    class Config:
        orm_mode = True
