from pydantic import BaseModel


class ReportUserXAgency(BaseModel):
    user_id: int
    agency_id: int

    class Config:
        orm_mode = True
