from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from training.schemas import Quiz
from training.repositories import QuizRepository
from training.api.deps import quiz_repository


router = APIRouter()


@router.get("/quizzes", response_model=List[Quiz])
def get_quizzes(repo: QuizRepository = Depends(quiz_repository)):
    return repo.find_all()


@router.get("/quizzes/{id}", response_model=Quiz)
def get_quiz(id: int, repo: QuizRepository = Depends(quiz_repository)):
    db_quiz = repo.find_by_id(id)
    if db_quiz is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_quiz
