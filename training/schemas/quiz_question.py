from pydantic import BaseModel

from training.schemas import QuizChoice


class QuizQuestionBase(BaseModel):
    text: str
    type: str
    choices: list[QuizChoice]


class QuizQuestionCreate(QuizQuestionBase):
    quiz_id: int


class QuizQuestion(QuizQuestionBase):
    id: int
    quiz_id: int

    class Config:
        orm_mode = True
