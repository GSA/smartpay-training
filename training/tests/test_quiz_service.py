from unittest.mock import MagicMock, patch
from training import models, schemas
from training.services import QuizService, AppError
from training.repositories import QuizRepository, QuizCompletionRepository


@patch.object(QuizRepository, "find_by_id")
@patch.object(QuizCompletionRepository, "create")
def test_grade_passing(
    mock_quiz_completion_repo_create: MagicMock,
    mock_quiz_repo_find_by_id: MagicMock,
    quiz_service: QuizService,
    valid_passing_submission: schemas.QuizSubmission,
    valid_quiz: models.Quiz
):
    mock_quiz_repo_find_by_id.return_value = valid_quiz
    mock_quiz_completion_repo_create.return_value = 0

    result = quiz_service.grade(quiz_id=123, user_id=123, submission=valid_passing_submission)

    assert result.success
    assert isinstance(result.value, schemas.QuizGrade)
    assert result.value.passed
    assert result.value.percentage == 1


@patch.object(QuizRepository, "find_by_id")
@patch.object(QuizCompletionRepository, "create")
def test_grade_failing(
    mock_quiz_completion_repo_create: MagicMock,
    mock_quiz_repo_find_by_id: MagicMock,
    quiz_service: QuizService,
    valid_failing_submission: schemas.QuizSubmission,
    valid_quiz: models.Quiz
):
    mock_quiz_repo_find_by_id.return_value = valid_quiz
    mock_quiz_completion_repo_create.return_value = 0

    result = quiz_service.grade(quiz_id=123, user_id=123, submission=valid_failing_submission)

    assert result.success
    assert isinstance(result.value, schemas.QuizGrade)
    assert not result.value.passed
    assert result.value.percentage == 0.5


@patch.object(QuizRepository, "find_by_id")
@patch.object(QuizCompletionRepository, "create")
def test_grade_invalid(
    mock_quiz_completion_repo_create: MagicMock,
    mock_quiz_repo_find_by_id: MagicMock,
    quiz_service: QuizService,
    invalid_submission: schemas.QuizSubmission,
    valid_quiz: models.Quiz
):
    mock_quiz_repo_find_by_id.return_value = valid_quiz
    mock_quiz_completion_repo_create.return_value = 0

    result = quiz_service.grade(quiz_id=123, user_id=123, submission=invalid_submission)

    assert not result.success
    assert isinstance(result.value, AppError)
    assert result.error.code == 422
