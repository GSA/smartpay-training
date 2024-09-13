from datetime import datetime
from pydantic import ConfigDict, BaseModel
from typing import Any


class QuizCompletionBase(BaseModel):
    quiz_id: int
    user_id: int
    passed: bool
    responses: dict[str, Any]


class QuizCompletionCreate(QuizCompletionBase):
    pass


class QuizCompletion(QuizCompletionBase):
    id: int
    submit_ts: datetime
    model_config = ConfigDict(from_attributes=True)
