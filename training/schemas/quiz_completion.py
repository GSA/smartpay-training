from datetime import datetime
from pydantic import BaseModel


class QuizCompletionBase(BaseModel):
    quiz_id: int
    user_id: int
    passed: bool


class QuizCompletionCreate(QuizCompletionBase):
    pass


class QuizCompletion(QuizCompletionBase):
    id: int
    submit_ts: datetime

    class Config:
        orm_mode = True
