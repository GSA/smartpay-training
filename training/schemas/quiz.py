from pydantic import BaseModel
from training.schemas import QuizContent, QuizContentCreate, QuizContentPublic


class QuizBase(BaseModel):
    name: str
    topic: str
    audience: str
    active: bool
    content: QuizContent


class QuizCreate(QuizBase):
    content: QuizContentCreate


class QuizPublic(QuizBase):
    id: int
    content: QuizContentPublic


class Quiz(QuizBase):
    id: int

    class Config:
        orm_mode = True
