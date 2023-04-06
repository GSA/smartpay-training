from pydantic import BaseModel


class QuizSubmissionQuestion(BaseModel):
    question_id: int
    response_ids: list[int]


class QuizSubmission(BaseModel):
    responses: list[QuizSubmissionQuestion]
