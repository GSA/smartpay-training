import pytest
from unittest.mock import MagicMock, patch
from training import models, schemas
from training.errors import SendEmailError
from training.repositories.gspc_invite import GspcInviteRepository
from training.services import GspcService
from training.repositories import CertificateRepository, GspcCompletionRepository
from sqlalchemy.orm import Session
from .factories import GspcCompletionFactory
from datetime import datetime

from ..api import email


@patch.object(GspcCompletionRepository, "create")
@patch.object(GspcService, "email_certificate")
@patch.object(GspcInviteRepository, "get_by_gspc_invite_id")
@patch.object(GspcInviteRepository, "set_completion_date")
def test_grade_passing(
        mock_gspc_completion_repo_create: MagicMock,
        mock_gspc_service_email_certificate: MagicMock,
        mock_gspc_invite_repo_get_by_gspc_invite_id: MagicMock,
        mock_gspc_invite_repo_set_completion_date: MagicMock,
        db_with_data: Session,
        valid_gspc_passing_submission: schemas.GspcCompletion,
        valid_user_ids,
):
    # Setup
    gspc_service = GspcService(db_with_data)

    date = datetime.now().replace(minute=0, hour=0, second=0, microsecond=0)
    expiration_date = date.replace(year=date.year + 100)
    user_id = valid_user_ids[-1]

    gspc_invite = models.GspcInvite(
        email='test3@example.com',
        certification_expiration_date=expiration_date,
        gspc_invite_id=valid_gspc_passing_submission.gspc_invite_id
    )

    gspc_completion = models.GspcCompletion(
        id=1,
        user_id=user_id,
        passed=True,
        certification_expiration_date=expiration_date,
        responses='',
        submit_ts=date,
        gspc_invite_id=valid_gspc_passing_submission.gspc_invite_id
    )

    gspc_service.gspc_invite_repo.get_by_gspc_invite_id = mock_gspc_invite_repo_get_by_gspc_invite_id
    mock_gspc_invite_repo_get_by_gspc_invite_id.return_value = gspc_invite

    gspc_service.email_certificate = mock_gspc_service_email_certificate
    mock_gspc_service_email_certificate.return_value = None

    gspc_service.gspc_invite_repo.set_completion_date = mock_gspc_invite_repo_set_completion_date
    mock_gspc_invite_repo_set_completion_date.return_value = None

    gspc_service.gspc_completion_repo.create = mock_gspc_completion_repo_create
    mock_gspc_completion_repo_create.return_value = gspc_completion

    # Execute
    result = gspc_service.grade(user_id, submission=valid_gspc_passing_submission)

    # Assert
    mock_gspc_invite_repo_get_by_gspc_invite_id.assert_called_once()
    mock_gspc_completion_repo_create.assert_called_once()
    mock_gspc_invite_repo_set_completion_date.assert_called_once()
    mock_gspc_service_email_certificate.assert_called_once()

    assert isinstance(result, schemas.GspcResult)
    assert result.passed
    assert result.cert_id == 1


@patch.object(GspcCompletionRepository, "create")
@patch.object(GspcInviteRepository, "get_by_gspc_invite_id")
@patch.object(GspcInviteRepository, "set_completion_date")
def test_grade_failing(
        mock_gspc_completion_repo_create: MagicMock,
        mock_gspc_invite_repo_get_by_gspc_invite_id: MagicMock,
        mock_gspc_invite_repo_set_completion_date: MagicMock,
        db_with_data: Session,
        valid_gspc_failing_submission: schemas.GspcCompletion,
        valid_user_ids,
):
    # Setup
    gspc_service = GspcService(db_with_data)

    date = datetime.now().replace(minute=0, hour=0, second=0, microsecond=0)
    expiration_date = date.replace(year=date.year + 100)
    user_id = valid_user_ids[-1]

    gspc_invite = models.GspcInvite(
        email='test3@example.com',
        certification_expiration_date=expiration_date,
        gspc_invite_id=valid_gspc_failing_submission.gspc_invite_id
    )

    gspc_completion = models.GspcCompletion(
        id=1,
        user_id=user_id,
        passed=True,
        certification_expiration_date=expiration_date,
        responses='',
        submit_ts=date,
        gspc_invite_id=valid_gspc_failing_submission.gspc_invite_id
    )

    gspc_service.gspc_invite_repo.get_by_gspc_invite_id = mock_gspc_invite_repo_get_by_gspc_invite_id
    mock_gspc_invite_repo_get_by_gspc_invite_id.return_value = gspc_invite

    gspc_service.gspc_invite_repo.set_completion_date = mock_gspc_invite_repo_set_completion_date
    mock_gspc_invite_repo_set_completion_date.return_value = None

    gspc_service.gspc_completion_repo.create = mock_gspc_completion_repo_create
    mock_gspc_completion_repo_create.return_value = gspc_completion

    # Execute
    result = gspc_service.grade(user_id, submission=valid_gspc_failing_submission)

    # Assert
    mock_gspc_invite_repo_get_by_gspc_invite_id.assert_called_once()
    mock_gspc_completion_repo_create.assert_called_once()
    mock_gspc_invite_repo_set_completion_date.assert_called_once()

    assert isinstance(result, schemas.GspcResult)
    assert not result.passed
    assert result.cert_id == 1


@patch.object(GspcCompletionRepository, "create")
@patch.object(CertificateRepository, "get_certificate_by_id")
@patch.object(GspcService, "email_certificate")
def test_grade_email_certificate_error(
        mock_gspc_service_email_certificate: MagicMock,
        mock_certificate_repo_get_certificate_by_id: MagicMock,
        mock_gspc_completion_repo_create: MagicMock,
        db_with_data: Session,
        valid_gspc_passing_submission: schemas.GspcSubmission,
        valid_gspc_certificate: schemas.GspcCertificate,
        valid_user_ids
):
    gspc_service = GspcService(db_with_data)

    user_id = valid_user_ids[-1]

    mock_gspc_completion_repo_create.return_value = GspcCompletionFactory.build()

    mock_certificate_repo_get_certificate_by_id.return_value = valid_gspc_certificate
    mock_gspc_service_email_certificate.side_effect = SendEmailError

    with pytest.raises(Exception):
        gspc_service.grade(user_id, submission=valid_gspc_passing_submission)


@patch.multiple(email.settings,
                SMTP_SERVER='email.example.com',
                SMTP_PORT=999,
                EMAIL_FROM='J.P.Nannetti@freemanjournal.com',
                EMAIL_FROM_NAME='Joseph Patrick Nannetti',
                SMTP_USER='Aeolus',
                SMTP_PASSWORD='cycl0ps'
                )
def test_email_certificate_config(
        db_with_data: Session,
        gspc_smtp_instance
):
    gspc_service = GspcService(db_with_data)
    gspc_service.email_certificate('Test_User', 'test_user@freemanjournal.com', b'')
    gspc_smtp_instance.starttls.assert_called()
    gspc_smtp_instance.login.assert_called_once_with(user='Aeolus', password='cycl0ps')


def test_email_certificate_passing(
        db_with_data: Session,
        gspc_smtp_instance
):
    gspc_service = GspcService(db_with_data)
    gspc_service.email_certificate('Test_User', 'test_user@freemanjournal.com', b'')
    args, _ = gspc_smtp_instance.send_message.call_args
    email_message = args[0]
    assert email_message['Subject'] == 'Certificate – GSA SmartPay® Program Certificate'
    assert email_message['To'] == 'test_user@freemanjournal.com'


def test_email_certificate_raises_exception(
        db_with_data: Session,
        gspc_smtp_instance
):
    gspc_service = GspcService(db_with_data)
    gspc_smtp_instance.send_message.side_effect = ValueError('something went wrong')
    with pytest.raises(SendEmailError):
        gspc_service.email_certificate('Test_User', 'test_user@freemanjournal.com', b'')
