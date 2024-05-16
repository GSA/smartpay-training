from datetime import datetime, timedelta
import pytest
from training import schemas
from training.repositories import GspcCompletionRepository


@pytest.fixture
def valid_gspc_completion(
    valid_user_ids: list[int]
) -> schemas.GspcCompletion:
    return schemas.GspcCompletion(
        user_id=valid_user_ids[-1],
        passed=True,
        certification_expiration_date='2099-01-01',
        responses={"responses": [{"correct": True, "question": "Q1", "response": "Yes", "question_id": 0, "response_id": 0}, {"correct": True, "question": "Q2", "response": "Yes", "question_id": 1, "response_id": 0}]}
    )


def test_create(
    gspc_completion_repo_with_data: GspcCompletionRepository,
    valid_gspc_completion: schemas.GspcCompletion,
):
    dt = datetime.utcnow()
    db_gspc_completion = gspc_completion_repo_with_data.create(valid_gspc_completion)
    assert db_gspc_completion.id
    assert db_gspc_completion.passed
    assert (dt - timedelta(minutes=5)) <= db_gspc_completion.submit_ts <= (dt + timedelta(minutes=5))
