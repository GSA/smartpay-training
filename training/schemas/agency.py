from typing import Optional
from pydantic import ConfigDict, BaseModel


class AgencyBase(BaseModel):
    name: str
    bureau: Optional[str] = None


class AgencyCreate(AgencyBase):
    pass


class Agency(AgencyBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class Bureau(BaseModel):
    id: int
    name: str


class AgencyWithBureaus(BaseModel):
    id: int
    name: str
    bureaus: list[Bureau]
