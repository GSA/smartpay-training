from pydantic import BaseModel
from training.schemas import QuizChoice, QuizChoicePublic, QuizChoiceCreate


class QuizQuestionBase(BaseModel):
    text: str
    type: str
    choices: list[QuizChoice]


class QuizQuestionCreate(QuizQuestionBase):
    choices: list[QuizChoiceCreate]


class QuizQuestionPublic(QuizQuestionBase):
    id: int
    choices: list[QuizChoicePublic]


class QuizQuestion(QuizQuestionBase):
    id: int

    class Config:
        orm_mode = True
