from datetime import datetime
from pydantic import BaseModel, ConfigDict
from training.schemas.user import UserBase


class UserQuizCompletionReportData(BaseModel):
    name: str
    email: str
    agency: str
    bureau: str | None = None
    quiz: str
    completion_date: datetime
    model_config = ConfigDict(from_attributes=True)

    # Add a custom constructor that accepts positional arguments
    def __init__(self, name, email, agency, bureau, quiz, completion_date, **kwargs):
        # Use the super() to call the BaseModel's __init__ with the correct keyword arguments
        super().__init__(
            name=name,
            email=email,
            agency=agency,
            bureau=bureau,
            quiz=quiz,
            completion_date=completion_date,
            **kwargs
        )


class AdminUserQuizCompletionReportData(UserBase):
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


class AdminUsersRolesReportData(BaseModel):
    name: str
    email: str
    assignedAgency: str
    assignedBureau: str | None = None
    adminRole: str
    reportRole: str
    reportAgency: str | None = None
    reportBureau: str | None = None
       