from datetime import datetime, timedelta, date
import uuid
import pytest
from unittest.mock import patch
from training.repositories import GspcInviteRepository
from training import models


@pytest.fixture
def mock_gspc_invite():
    invite_id = uuid.uuid4()
    return models.GspcInvite(
        email="test@example.gov",
        gspc_invite_id=invite_id,
        certification_expiration_date=date(2099, 1, 1)
    )


def test_create(gspc_invite_repo_with_data: GspcInviteRepository):
    """Tests creation of a single GspcInvite"""
    # Execute
    email = "test@example.gov"
    expiration_date = date(2099, 1, 1)
    result = gspc_invite_repo_with_data.create(email, expiration_date)

    # Assert
    assert result.email == email
    assert result.certification_expiration_date == expiration_date
    assert isinstance(result.gspc_invite_id, uuid.UUID)


def test_bulk_create(gspc_invite_repo_with_data: GspcInviteRepository):
    """Tests bulk creation of GspcInvites"""

    # Mock time.sleep
    with patch("time.sleep"):
        # Execute
        emails = ["test1@example.gov", "test2@example.gov", "test3@example.gov", "test4@example.gov"]
        expiration_date = date(2099, 1, 1)
        result = gspc_invite_repo_with_data.bulk_create(emails, expiration_date)

    # Assert
    assert len(result) == 4
    for i, invite in enumerate(result):
        assert invite.email == emails[i]
        assert invite.certification_expiration_date == expiration_date
        assert isinstance(invite.gspc_invite_id, uuid.UUID)


def test_batch_iterator():
    """Tests the batch_iterator static method"""
    items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    batch_size = 3

    batches = list(GspcInviteRepository.batch_iterator(items, batch_size))

    assert len(batches) == 4
    assert batches[0] == [1, 2, 3]
    assert batches[1] == [4, 5, 6]
    assert batches[2] == [7, 8, 9]
    assert batches[3] == [10]


def test_get_by_gspc_invite_id(gspc_invite_repo_with_data: GspcInviteRepository):
    """Tests retrieving an invite by UUID"""
    email = "test@example.gov"
    expiration_date = date(2099, 1, 1)
    create_result = gspc_invite_repo_with_data.create(email, expiration_date)

    # Execute
    result = gspc_invite_repo_with_data.get_by_gspc_invite_id(create_result.gspc_invite_id)

    # Assert
    assert result == create_result


def test_get_by_gspc_invite_id_not_found(gspc_invite_repo_with_data: GspcInviteRepository):
    """Tests exception when invite UUID not found"""
    # Setup
    invite_id = uuid.uuid4()

    # Execute & Assert
    with pytest.raises(ValueError, match="No invite found with the given gspc_invite_id"):
        gspc_invite_repo_with_data.get_by_gspc_invite_id(invite_id)


def test_get_invites_for_second_follow_up(gspc_invite_repo_without_data: GspcInviteRepository):
    """Tests retrieving and updating invites eligible for second follow-up"""
    # Setup
    current_time = datetime.now()

    # Create mock invites that match criteria
    mock_invites = [
        models.GspcInvite(
            id=1,
            email="test1@example.gov",
            gspc_invite_id=uuid.uuid4(),
            created_date=current_time - timedelta(days=2),
            certification_expiration_date=date(2099, 1, 1),
            second_invite_date=None,
            completed_date=None
        ),
        models.GspcInvite(
            id=2,
            email="test2@example.gov",
            gspc_invite_id=uuid.uuid4(),
            created_date=current_time - timedelta(days=3),
            certification_expiration_date=date(2099, 1, 1),
            second_invite_date=None,
            completed_date=None
        ),
        models.GspcInvite(
            id=3,
            email="test1@example.gov",
            gspc_invite_id=uuid.uuid4(),
            created_date=current_time - timedelta(days=10),
            second_invite_date=current_time - timedelta(days=2),
            certification_expiration_date=date(2099, 1, 1),
            final_invite_date=None,
            completed_date=current_time
        ),
    ]

    gspc_invite_repo_without_data.bulk_save(mock_invites)

    # Execute
    results = gspc_invite_repo_without_data.get_invites_for_second_follow_up()

    # Assert
    assert len(results) == 2


def test_get_invites_for_final_follow_up(gspc_invite_repo_without_data: GspcInviteRepository):
    """Tests retrieving and updating invites eligible for final follow-up"""
    # Setup
    current_time = datetime.now()

    # Create mock invites that match criteria
    mock_invites = [
        # valid
        models.GspcInvite(
            id=1,
            email="test1@example.gov",
            gspc_invite_id=uuid.uuid4(),
            created_date=current_time - timedelta(days=2),
            certification_expiration_date=date(2099, 1, 1),
            second_invite_date=current_time - timedelta(days=2),
            completed_date=None
        ),
        # invalid hasn't had second invite
        models.GspcInvite(
            id=2,
            email="test2@example.gov",
            gspc_invite_id=uuid.uuid4(),
            created_date=current_time - timedelta(days=3),
            certification_expiration_date=date(2099, 1, 1),
            second_invite_date=None,
            completed_date=None
        ),
        # invalid completed
        models.GspcInvite(
            id=3,
            email="test1@example.gov",
            gspc_invite_id=uuid.uuid4(),
            created_date=current_time - timedelta(days=10),
            second_invite_date=current_time - timedelta(days=2),
            certification_expiration_date=date(2099, 1, 1),
            final_invite_date=None,
            completed_date=current_time
        ),
        # invalid already sent final
        models.GspcInvite(
            id=4,
            email="test1@example.gov",
            gspc_invite_id=uuid.uuid4(),
            created_date=current_time - timedelta(days=10),
            second_invite_date=current_time - timedelta(days=2),
            certification_expiration_date=date(2099, 1, 1),
            final_invite_date=current_time - timedelta(days=2),
            completed_date=None
        ),
    ]

    gspc_invite_repo_without_data.bulk_save(mock_invites)

    # Execute
    results = gspc_invite_repo_without_data.get_invites_for_second_follow_up()

    # Assert
    assert len(results) == 1


def test_set_completion_date(gspc_invite_repo_without_data: GspcInviteRepository):
    """Tests setting completion date for an invite"""
    # Setup
    email = "test@example.gov"
    expiration_date = date(2099, 1, 1)
    obj = gspc_invite_repo_without_data.create(email, expiration_date)

    gspc_invite_repo_without_data.set_completion_date(obj.id)

    obj = gspc_invite_repo_without_data.find_by_id(obj.id)

    # Assert
    assert obj.completed_date is not None


def test_set_completion_date_invalid_id(gspc_invite_repo_without_data: GspcInviteRepository):
    """Tests error when setting completion date with invalid id"""
    # Setup
    invite_id = 999  # Non-existent ID

    # Execute & Assert
    with pytest.raises(ValueError, match="invalid gspc invite id"):
        gspc_invite_repo_without_data.set_completion_date(invite_id)
