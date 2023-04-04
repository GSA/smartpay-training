from pydantic import BaseModel


class QuizChoiceBase(BaseModel):
    text: str
    correct: bool


class QuizChoiceCreate(QuizChoiceBase):
    question_id: int


class QuizChoice(QuizChoiceBase):
    id: int
    question_id: int

    class Config:
        orm_mode = True
