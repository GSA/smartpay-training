from datetime import datetime
from pydantic import BaseModel, ConfigDict
from training.schemas.user import UserBase


class UserQuizCompletionReportData(UserBase):
    agency: str
    bureau: str | None = None
    quiz: str
    completion_date: datetime
    model_config = ConfigDict(from_attributes=True)


class GspcCompletionReportData(BaseModel):
    invitedEmail: str | None = None
    registeredEmail: str | None = None
    username: str | None = None
    agency: str | None = None
    bureau: str | None = None
    passed: bool | None = None
    completionDate: datetime | None = None
    model_config = ConfigDict(from_attributes=True)
