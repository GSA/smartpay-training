from pydantic import ConfigDict, BaseModel


class ReportUserXAgency(BaseModel):
    user_id: int
    agency_id: int
    model_config = ConfigDict(from_attributes=True)
