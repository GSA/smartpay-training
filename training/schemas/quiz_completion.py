from datetime import datetime
from pydantic import ConfigDict, BaseModel


class QuizCompletionBase(BaseModel):
    quiz_id: int
    user_id: int
    passed: bool


class QuizCompletionCreate(QuizCompletionBase):
    pass


class QuizCompletion(QuizCompletionBase):
    id: int
    submit_ts: datetime
    model_config = ConfigDict(from_attributes=True)
