from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from training.schemas import Quiz, QuizGrade, QuizSubmission
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


@router.post("/quizzes/{id}/submission", response_model=QuizGrade)
def submit_quiz(id: int, submission: QuizSubmission, repo: QuizRepository = Depends(quiz_repository)):
    quiz = repo.find_by_id(id)
    if quiz is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")

    correct_count = 0
    question_count = len(quiz.questions)
    questions = []

    for question in quiz.questions:
        # From the submission, get the response matching the current question
        response = next((r for r in submission.responses if r.question_id == question.id), None)
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"No responses given for question ID {question.id}"
            )

        # Get a list of correct choice IDs from the answer sheet
        correct_ids = [choice.id for choice in question.choices if choice.correct]

        # Verify whether the set of response IDs match the correct choice IDs
        response_correct = set(correct_ids) == set(response.response_ids)
        if response_correct:
            correct_count += 1

        # Mark the question response as correct or incorrect
        questions.append({
            "question_id": question.id,
            "correct": response_correct
        })

    grade = QuizGrade(
        quiz_id=id,
        correct_count=correct_count,
        question_count=question_count,
        percentage=(correct_count / question_count),
        passed=((correct_count / question_count) > 0.75),
        questions=questions,
    )

    return grade
