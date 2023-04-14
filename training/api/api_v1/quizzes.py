from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from training.schemas import Quiz, QuizPublic, QuizGrade, QuizSubmission, QuizCreate
from training.repositories import QuizRepository
from training.services import QuizService
from training.api.deps import quiz_repository, quiz_service


router = APIRouter()


@router.post("/quizzes", response_model=Quiz, status_code=status.HTTP_201_CREATED)
def create_quiz(quiz: QuizCreate, repo: QuizRepository = Depends(quiz_repository)):
    db_quiz = repo.create(quiz)
    return db_quiz


@router.get("/quizzes", response_model=List[QuizPublic])
def get_quizzes(
    topic: str | None = None,
    audience: str | None = None,
    active: bool | None = None,
    repo: QuizRepository = Depends(quiz_repository)
):
    filters = {}
    if topic is not None:
        filters["topic"] = topic
    if audience is not None:
        filters["audience"] = audience
    if active is not None:
        filters["active"] = active
    return repo.find_all(filters=filters)


@router.get("/quizzes/{id}", response_model=QuizPublic)
def get_quiz(id: int, repo: QuizRepository = Depends(quiz_repository)):
    quiz = repo.find_by_id(id)
    if quiz is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return quiz


@router.post("/quizzes/{id}/submission", response_model=QuizGrade)
def submit_quiz(
    id: int,
    submission: QuizSubmission,
    quiz_service: QuizService = Depends(quiz_service)
):
    grade_result = quiz_service.grade(quiz_id=id, user_id=1, submission=submission)
    if not grade_result.success:
        raise HTTPException(
            status_code=grade_result.error.code,
            detail=grade_result.error.message
        )
    return grade_result.value
