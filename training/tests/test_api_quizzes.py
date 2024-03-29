import pytest
from fastapi.testclient import TestClient
from fastapi import status
from training.errors import IncompleteQuizResponseError, QuizNotFoundError
from training.main import app
from training.repositories import QuizRepository
from training.schemas import QuizCreate
from training.services import QuizService
from .factories import QuizCreateSchemaFactory, QuizGradeSchemaFactory, QuizSchemaFactory, QuizSubmissionSchemaFactory


client = TestClient(app)


@pytest.mark.skip(reason="quiz creation disabled for now")
def test_create_quiz_valid(
    valid_quiz_create: QuizCreate,
    mock_quiz_repo: QuizRepository
):
    mock_quiz_repo.create.return_value = QuizSchemaFactory.build()
    response = client.post(
        "/api/v1/quizzes",
        json=valid_quiz_create.model_dump()
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.skip(reason="quiz creation disabled for now")
def test_create_quiz_invalid():
    quiz_create = QuizCreateSchemaFactory.build()
    quiz_create.audience = "Invalid"  # type: ignore
    response = client.post(
        "/api/v1/quizzes",
        json=quiz_create.model_dump()
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_quizzes(mock_quiz_repo: QuizRepository):
    mock_quiz_repo.find_all.return_value = [QuizSchemaFactory.build()]
    response = client.get(
        "/api/v1/quizzes"
    )
    assert response.status_code == status.HTTP_200_OK


def test_get_quizzes_filtered(mock_quiz_repo: QuizRepository):
    mock_quiz_repo.find_all.return_value = [QuizSchemaFactory.build()]
    filters = {}
    filters["topic"] = "Travel"
    response = client.get(
        "/api/v1/quizzes?topic=Travel"
    )
    assert response.status_code == status.HTTP_200_OK
    mock_quiz_repo.find_all.assert_called_with(filters=filters)


def test_get_quiz(mock_quiz_repo: QuizRepository):
    mock_quiz_repo.find_by_id.return_value = QuizSchemaFactory.build()
    response = client.get(
        "/api/v1/quizzes/1"
    )
    assert response.status_code == status.HTTP_200_OK
    mock_quiz_repo.find_by_id.assert_called_with(1)


def test_get_quiz_invalid_id(mock_quiz_repo: QuizRepository):
    mock_quiz_repo.find_by_id.return_value = None
    response = client.get(
        "/api/v1/quizzes/1"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    mock_quiz_repo.find_by_id.assert_called_with(1)


def test_submit_quiz(mock_quiz_service: QuizService, valid_jwt: str):
    mock_quiz_service.grade.return_value = QuizGradeSchemaFactory.build()
    response = client.post(
        "/api/v1/quizzes/1/submission",
        json=QuizSubmissionSchemaFactory.build().model_dump(),
        headers={"Authorization": f"Bearer {valid_jwt}"}
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_submit_quiz_invalid_id(mock_quiz_service: QuizService, valid_jwt: str):
    mock_quiz_service.grade.side_effect = QuizNotFoundError
    response = client.post(
        "/api/v1/quizzes/1/submission",
        json=QuizSubmissionSchemaFactory.build().model_dump(),
        headers={"Authorization": f"Bearer {valid_jwt}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_submit_quiz_incomplete(mock_quiz_service: QuizService, valid_jwt: str):
    mock_quiz_service.grade.side_effect = IncompleteQuizResponseError([0, 1, 2])
    response = client.post(
        "/api/v1/quizzes/1/submission",
        json=QuizSubmissionSchemaFactory.build().model_dump(),
        headers={"Authorization": f"Bearer {valid_jwt}"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
