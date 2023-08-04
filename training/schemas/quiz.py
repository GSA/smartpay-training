from enum import Enum
from pydantic import BaseModel
from training.schemas import QuizContent, QuizContentCreate, QuizContentPublic


class QuizTopic(str, Enum):
    Travel = "Travel"
    Purchase = "Purchase"
    Fleet = "Fleet"


class QuizAudience(str, Enum):
    AccountHoldersApprovingOfficials = "AccountHoldersApprovingOfficials"
    ProgramCoordinators = "ProgramCoordinators"


class QuizBase(BaseModel):
    name: str
    topic: QuizTopic
    audience: QuizAudience
    active: bool
    content: QuizContent


class QuizCreate(QuizBase):
    content: QuizContentCreate


class QuizPublic(QuizBase):
    id: int
    content: QuizContentPublic

    class Config:
        orm_mode = True


class Quiz(QuizBase):
    id: int

    class Config:
        orm_mode = True
