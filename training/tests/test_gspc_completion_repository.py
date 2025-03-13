from datetime import datetime, timedelta
import pytest
from training.repositories import GspcCompletionRepository
from training import schemas
from training.repositories.gspc_invite import GspcInviteRepository
from sqlalchemy.orm import Session


# Define mock models directly in the test function
class MockGspcCompletion:
    def __init__(self, invitedEmail, registeredEmail, username, agency, bureau, passed, completionDate):
        self.invitedEmail = invitedEmail
        self.registeredEmail = registeredEmail
        self.username = username
        self.agency = agency
        self.bureau = bureau
        self.passed = passed
        self.completionDate = completionDate


@pytest.fixture
def valid_gspc_completion(valid_user_ids: list[int]) -> schemas.GspcCompletion:
    return schemas.GspcCompletion(
        user_id=valid_user_ids[-1],
        passed=True,
        certification_expiration_date='2099-01-01',
        gspc_invite_id='55383009-B616-4ABF-A807-3585A716C5A6',  # placeholder
        responses={"responses": [
            {"correct": True, "question": "Q1", "response": "Yes", "question_id": 0, "response_id": 0},
            {"correct": True, "question": "Q2", "response": "Yes", "question_id": 1, "response_id": 0}
        ]}
    )


def test_create(
    db_with_data: Session,
    valid_gspc_completion: schemas.GspcCompletion,
):
    '''Creates a new record'''
    # Setup
    # add invite record for fk constraint
    invite_repo = GspcInviteRepository(db_with_data)
    completion_repo = GspcCompletionRepository(db_with_data)

    invite = invite_repo.create("test@test.com", valid_gspc_completion.certification_expiration_date)
    valid_gspc_completion.gspc_invite_id = invite.gspc_invite_id

    # Execute
    db_gspc_completion = completion_repo.create(valid_gspc_completion)

    # Assert
    assert db_gspc_completion.id
    assert db_gspc_completion.passed

    dt = datetime.utcnow()
    assert (dt - timedelta(minutes=5)) <= db_gspc_completion.submit_ts <= (dt + timedelta(minutes=5))
