from datetime import datetime, timedelta
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
        passed=True,
        responses=dict([{'question_id': 0, 'response_ids': [1]}, {'question_id': 1, 'response_ids': [1]}, {'question_id': 2, 'response_ids': [2]}])
    )


def test_create(
    quiz_completion_repo_with_data: QuizCompletionRepository,
    valid_quiz_completion_create: schemas.QuizCompletionCreate,
):
    dt = datetime.utcnow()
    db_quiz_completion = quiz_completion_repo_with_data.create(valid_quiz_completion_create)
    assert db_quiz_completion.id
    assert db_quiz_completion.passed
    assert (dt - timedelta(minutes=5)) <= db_quiz_completion.submit_ts <= (dt + timedelta(minutes=5))
