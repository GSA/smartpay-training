from datetime import datetime, timedelta
import pytest
from unittest.mock import MagicMock, patch
from training.repositories import GspcCompletionRepository
from sqlalchemy.orm import Session
from training import schemas


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
        responses={"responses": [
            {"correct": True, "question": "Q1", "response": "Yes", "question_id": 0, "response_id": 0},
            {"correct": True, "question": "Q2", "response": "Yes", "question_id": 1, "response_id": 0}
        ]}
    )


def test_create(
    gspc_completion_repo_with_data: GspcCompletionRepository,
    valid_gspc_completion: schemas.GspcCompletion,
):
    '''Creates a new record'''
    dt = datetime.utcnow()
    db_gspc_completion = gspc_completion_repo_with_data.create(valid_gspc_completion)
    assert db_gspc_completion.id
    assert db_gspc_completion.passed
    assert (dt - timedelta(minutes=5)) <= db_gspc_completion.submit_ts <= (dt + timedelta(minutes=5))


@patch('training.repositories.GspcCompletionRepository._get_completed_gspc_results')
@patch('training.repositories.GspcCompletionRepository._get_uncompleted_gspc_results')
def test_get_gspc_completion_report(mock_get_uncompleted_gspc_results, mock_get_completed_gspc_results):
    '''Gets result from both queries and return them in a list'''
    # Create mock data for completed and uncompleted results
    completedGspcResults = [
        MockGspcCompletion(invitedEmail='invite1@example.com', registeredEmail='user1@example.com',
                           username='User1', agency='Agency1', bureau='Bureau1', passed=True, completionDate=datetime(2024, 1, 1, 12, 0, 0)),
        MockGspcCompletion(invitedEmail='invite2@example.com', registeredEmail='user2@example.com',
                           username='User2', agency='Agency2', bureau='Bureau2', passed=False, completionDate=datetime(2024, 1, 2, 12, 0, 0)),
    ]

    uncompletedGspcResults = [
        MockGspcCompletion(invitedEmail='invite3@example.com', registeredEmail=None, username=None, agency=None, bureau=None, passed=None, completionDate=None),
    ]

    # Mock the return values for the sub-methods
    mock_get_completed_gspc_results.return_value = completedGspcResults
    mock_get_uncompleted_gspc_results.return_value = uncompletedGspcResults

    # Instantiate the repository with a mock session
    mock_db_session = MagicMock(spec=Session)
    repo = GspcCompletionRepository(mock_db_session)

    # Call the method
    results = repo.get_gspc_completion_report()

    # Check the results
    assert len(results) == 3

    # Check the completed results
    firstResult = results[0]
    assert firstResult.invitedEmail == 'invite1@example.com'
    assert firstResult.registeredEmail == 'user1@example.com'
    assert firstResult.username == 'User1'
    assert firstResult.agency == 'Agency1'
    assert firstResult.bureau == 'Bureau1'
    assert firstResult.passed
    assert firstResult.completionDate == datetime(2024, 1, 1, 12, 0, 0)

    secondRow = results[1]
    assert secondRow.invitedEmail == 'invite2@example.com'
    assert secondRow.registeredEmail == 'user2@example.com'
    assert secondRow.username == 'User2'
    assert secondRow.agency == 'Agency2'
    assert secondRow.bureau == 'Bureau2'
    assert secondRow.passed is False
    assert secondRow.completionDate == datetime(2024, 1, 2, 12, 0, 0)

    # Check the uncompleted results
    thirdRow = results[2]
    assert thirdRow.invitedEmail == 'invite3@example.com'
    assert thirdRow.registeredEmail is None
    assert thirdRow.username is None
    assert thirdRow.agency is None
    assert thirdRow.bureau is None
    assert thirdRow.passed is None
    assert thirdRow.completionDate is None


# Testing the private methods directly
def test_get_completed_gspc_results():
    '''Returns completed_gspc_results'''
    mock_db_session = MagicMock(spec=Session)
    repo = GspcCompletionRepository(mock_db_session)

    completedGspcResults = [
        MockGspcCompletion(invitedEmail='invite1@example.com', registeredEmail='user1@example.com',
                           username='User1', agency='Agency1', bureau='Bureau1', passed=True, completionDate=datetime(2024, 1, 1, 12, 0, 0)),
        MockGspcCompletion(invitedEmail='invite2@example.com', registeredEmail='user2@example.com',
                           username='User2', agency='Agency2', bureau='Bureau2', passed=False, completionDate=datetime(2024, 1, 2, 12, 0, 0)),
    ]

    mock_query = MagicMock()
    mock_query.select_from.return_value = mock_query
    mock_query.join.return_value = mock_query
    mock_query.outerjoin.return_value = mock_query
    mock_query.distinct.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.all.return_value = completedGspcResults
    mock_db_session.query.return_value = mock_query

    results = repo._get_completed_gspc_results()

    assert len(results) == 2
    assert results[0].invitedEmail == 'invite1@example.com'
    assert results[1].invitedEmail == 'invite2@example.com'


def test_get_uncompleted_gspc_results():
    '''Returns uncompleted_gspc_results'''
    mock_db_session = MagicMock(spec=Session)
    repo = GspcCompletionRepository(mock_db_session)

    uncompletedGspcResults = [
        MockGspcCompletion(invitedEmail='invite3@example.com', registeredEmail=None, username=None, agency=None, bureau=None, passed=None, completionDate=None),
    ]

    mock_query = MagicMock()
    mock_query.select_from.return_value = mock_query
    mock_query.outerjoin.return_value = mock_query
    mock_query.distinct.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = uncompletedGspcResults
    mock_db_session.query.return_value = mock_query

    results = repo._get_uncompleted_gspc_results()

    # Assert the results
    assert len(results) == 1
    assert results[0].invitedEmail == 'invite3@example.com'
    assert results[0].registeredEmail is None
    assert results[0].username is None
    assert results[0].agency is None
    assert results[0].bureau is None
    assert results[0].passed is None
    assert results[0].completionDate is None
