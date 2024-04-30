from pydantic import BaseModel


class GspcSubmissionQuestion(BaseModel):
    question_id: int
    question: str
    response_id: int
    response: str
    correct: bool


class GspcSubmission(BaseModel):
    expiration_date: str
    responses: list[GspcSubmissionQuestion]
