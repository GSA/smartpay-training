from datetime import datetime
from pydantic import ConfigDict, BaseModel
from enum import Enum


class CertificateType(Enum):
    QUIZ = 1
    GSPC = 2


class CertificateListValue(BaseModel):
    id: int
    user_id: int
    user_name: str
    cert_title: str
    completion_date: datetime
    certificate_type: CertificateType


class UserCertificate(BaseModel):
    id: int
    user_id: int
    user_name: str
    quiz_id: int
    quiz_name: str
    agency: str
    completion_date: datetime
    model_config = ConfigDict(from_attributes=True)
