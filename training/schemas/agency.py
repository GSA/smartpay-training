from pydantic import BaseModel
from pydantic.schema import Optional


class AgencyBase(BaseModel):
    name: str
    bureau: Optional[str]


class AgencyCreate(AgencyBase):
    pass


class Agency(AgencyBase):
    id: int

    class Config:
        orm_mode = True


class Bureau(BaseModel):
    id: int
    name: str


class AgencyWithBureaus(BaseModel):
    id: int
    name: str
    bureaus: list[Bureau]
