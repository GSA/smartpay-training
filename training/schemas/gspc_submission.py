from pydantic import BaseModel


class QuizSubmissionQuestion(BaseModel):
    question_id: int
    question: str
    response_ids: list[int]
    response: list[str]
    correct: bool


class GspcSubmission(BaseModel):
    responses: list[QuizSubmissionQuestion]
