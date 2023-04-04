from pydantic import BaseModel

from training.schemas import QuizQuestion


class QuizBase(BaseModel):
    name: str
    topic: str
    audience: str
    active: bool
    questions: list[QuizQuestion]


class QuizCreate(QuizBase):
    pass


class Quiz(QuizBase):
    id: int

    class Config:
        orm_mode = True
