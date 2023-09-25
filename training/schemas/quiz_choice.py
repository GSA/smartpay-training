from pydantic import ConfigDict, BaseModel


class QuizChoiceBase(BaseModel):
    text: str


class QuizChoiceCreate(QuizChoiceBase):
    correct: bool


class QuizChoicePublic(QuizChoiceBase):
    id: int


class QuizChoice(QuizChoiceBase):
    id: int
    correct: bool
    model_config = ConfigDict(from_attributes=True)
