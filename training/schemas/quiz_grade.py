from pydantic import BaseModel


class QuizGradeQuestion(BaseModel):
    question_id: int
    correct: bool
    selected_ids: list[int]
    correct_ids: list[int]


class QuizGrade(BaseModel):
    quiz_id: int
    correct_count: int
    question_count: int
    percentage: float
    passed: bool
    questions: list[QuizGradeQuestion]
