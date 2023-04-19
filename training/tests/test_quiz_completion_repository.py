from datetime import datetime
import pytest
from training import schemas
from training.repositories import QuizCompletionRepository


@pytest.fixture
def valid_quiz_completion_create(
    valid_quiz_ids: list[int],
    valid_user_ids: list[int]
) -> schemas.QuizCompletionCreate:
    return schemas.QuizCompletionCreate(
        quiz_id=valid_quiz_ids[-1],
        user_id=valid_user_ids[-1],
        passed=True
    )


def test_create(
    quiz_completion_repo_with_data: QuizCompletionRepository,
    valid_quiz_completion_create: schemas.QuizCompletionCreate,
):
    start = datetime.utcnow()
    start = start.replace(second=(start.second - 1))
    db_quiz_completion = quiz_completion_repo_with_data.create(valid_quiz_completion_create)
    end = datetime.utcnow()
    end = end.replace(second=(end.second + 1))
    assert db_quiz_completion.id
    assert db_quiz_completion.passed
    assert start <= db_quiz_completion.submit_ts <= end


