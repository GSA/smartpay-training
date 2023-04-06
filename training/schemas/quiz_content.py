from pydantic import BaseModel
from training.schemas import QuizQuestion, QuizQuestionPublic, QuizQuestionCreate


class QuizContent(BaseModel):
    questions: list[QuizQuestion]


class QuizContentCreate(BaseModel):
    questions: list[QuizQuestionCreate]


class QuizContentPublic(BaseModel):
    questions: list[QuizQuestionPublic]
