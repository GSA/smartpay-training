from datetime import datetime
from pydantic import ConfigDict, BaseModel


class UserCertificate(BaseModel):
    id: int
    user_id: int
    user_name: str
    quiz_id: int
    quiz_name: str
    completion_date: datetime
    model_config = ConfigDict(from_attributes=True)
