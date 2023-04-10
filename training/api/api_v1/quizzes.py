from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from training.schemas import Quiz, QuizPublic, QuizGrade, QuizSubmission, QuizCreate
from training.repositories import QuizRepository
from training.api.deps import quiz_repository


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
def submit_quiz(id: int, submission: QuizSubmission, repo: QuizRepository = Depends(quiz_repository)):
    db_quiz = repo.find_by_id(id)
    if db_quiz is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")

    quiz = Quiz.from_orm(db_quiz)
    correct_count = 0
    question_count = len(quiz.content.questions)
    questions = []

    for question in quiz.content.questions:
        # From the submission, get the response matching the current question
        response = next((r for r in submission.responses if r.question_id == question.id), None)
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f'No response(s) given for question ID {question.id}'
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
