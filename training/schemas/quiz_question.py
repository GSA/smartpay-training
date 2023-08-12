from enum import Enum
from pydantic import ConfigDict, BaseModel
from training.schemas import QuizChoice, QuizChoicePublic, QuizChoiceCreate


class QuizQuestionType(str, Enum):
    MultipleChoiceMultipleSelect = "MultipleChoiceMultipleSelect"
    MultipleChoiceSingleSelect = "MultipleChoiceSingleSelect"


class QuizQuestionBase(BaseModel):
    text: str
    type: QuizQuestionType
    choices: list[QuizChoice]


class QuizQuestionCreate(QuizQuestionBase):
    choices: list[QuizChoiceCreate]


class QuizQuestionPublic(QuizQuestionBase):
    id: int
    choices: list[QuizChoicePublic]


class QuizQuestion(QuizQuestionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
