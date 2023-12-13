import pytest
from unittest.mock import MagicMock, patch
from training import models, schemas
from training.errors import IncompleteQuizResponseError, SendEmailError
from training.services import QuizService
from training.repositories import QuizRepository, QuizCompletionRepository, CertificateRepository
from sqlalchemy.orm import Session
from .factories import QuizCompletionFactory
from unittest.mock import ANY

from ..api import email


@patch.object(QuizCompletionRepository, "create")
@patch.object(CertificateRepository, "get_certificate_by_id")
@patch.object(QuizService, "email_certificate")
def test_grade_passing(
        mock_quiz_service_email_certificate: MagicMock,
        mock_certificate_repo_get_certificate_by_id: MagicMock,
        mock_quiz_completion_repo_create: MagicMock,
        db_with_data: Session,
        valid_passing_submission: schemas.QuizSubmission,
        valid_user_certificate: schemas.UserCertificate,
        valid_user_ids,
        valid_quiz_ids
):
    quiz_service = QuizService(db_with_data)

    user_id = valid_user_ids[-1]
    quiz_id = valid_quiz_ids[0]

    mock_quiz_completion_repo_create.return_value = QuizCompletionFactory.build()

    mock_certificate_repo_get_certificate_by_id.return_value = valid_user_certificate
    mock_quiz_service_email_certificate.return_value = None

    result = quiz_service.grade(quiz_id, user_id, submission=valid_passing_submission)

    mock_quiz_service_email_certificate.assert_called_once_with(
        "Test Three",
        "Travel Training for Ministry of Magic",
        "test3@example.com",
        ANY
    )

    assert isinstance(result, schemas.QuizGrade)
    assert result.passed
    assert result.percentage == 1
    assert result.questions[0].correct_ids == [0]
    assert result.questions[0].selected_ids == [0]
    assert result.questions[1].correct_ids == [1]
    assert result.questions[1].selected_ids == [1]


@patch.object(QuizRepository, "find_by_id")
@patch.object(QuizCompletionRepository, "create")
def test_grade_failing(
        mock_quiz_completion_repo_create: MagicMock,
        mock_quiz_repo_find_by_id: MagicMock,
        db_with_data: Session,
        valid_failing_submission: schemas.QuizSubmission,
        valid_quiz: models.Quiz
):
    quiz_service = QuizService(db_with_data)
    mock_quiz_repo_find_by_id.return_value = valid_quiz
    mock_quiz_completion_repo_create.return_value = QuizCompletionFactory.build()

    result = quiz_service.grade(quiz_id=123, user_id=123, submission=valid_failing_submission)

    assert isinstance(result, schemas.QuizGrade)
    assert not result.passed
    assert result.percentage == 0.5
    assert result.questions[0].correct_ids == []
    assert result.questions[0].selected_ids == [1]
    assert result.questions[1].correct_ids == []
    assert result.questions[1].selected_ids == [1]


@patch.object(QuizRepository, "find_by_id")
@patch.object(QuizCompletionRepository, "create")
def test_grade_invalid(
        mock_quiz_completion_repo_create: MagicMock,
        mock_quiz_repo_find_by_id: MagicMock,
        db_with_data: Session,
        invalid_submission: schemas.QuizSubmission,
        valid_quiz: models.Quiz
):
    quiz_service = QuizService(db_with_data)
    mock_quiz_repo_find_by_id.return_value = valid_quiz
    mock_quiz_completion_repo_create.return_value = 0

    with pytest.raises(IncompleteQuizResponseError) as err:
        quiz_service.grade(quiz_id=123, user_id=123, submission=invalid_submission)

    assert err.value.missing_responses == [1]


@patch.object(QuizCompletionRepository, "create")
@patch.object(CertificateRepository, "get_certificate_by_id")
@patch.object(QuizService, "email_certificate")
def test_grade_email_certificate_error(
        mock_quiz_service_email_certificate: MagicMock,
        mock_certificate_repo_get_certificate_by_id: MagicMock,
        mock_quiz_completion_repo_create: MagicMock,
        db_with_data: Session,
        valid_passing_submission: schemas.QuizSubmission,
        valid_user_certificate: schemas.UserCertificate,
        valid_user_ids,
        valid_quiz_ids
):
    quiz_service = QuizService(db_with_data)

    user_id = valid_user_ids[-1]
    quiz_id = valid_quiz_ids[0]

    mock_quiz_completion_repo_create.return_value = QuizCompletionFactory.build()

    mock_certificate_repo_get_certificate_by_id.return_value = valid_user_certificate
    mock_quiz_service_email_certificate.side_effect = SendEmailError

    with pytest.raises(Exception):
        quiz_service.grade(quiz_id, user_id, submission=valid_passing_submission)


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
        smtp_instance
):
    quiz_service = QuizService(db_with_data)
    quiz_service.email_certificate('Test_User', 'Travel Training for Ministry of Magic', 'test_user@freemanjournal.com', b'')
    smtp_instance.starttls.assert_called()
    smtp_instance.login.assert_called_once_with(user='Aeolus', password='cycl0ps')


def test_email_certificate_passing(
        db_with_data: Session,
        smtp_instance
):
    quiz_service = QuizService(db_with_data)
    quiz_service.email_certificate('Test_User', 'Travel Training for Ministry of Magic', 'test_user@freemanjournal.com', b'')
    args, _ = smtp_instance.send_message.call_args
    email_message = args[0]
    assert email_message['Subject'] == 'Certificate - GSA SmartPay Travel Training for Ministry of Magic'
    assert email_message['To'] == 'test_user@freemanjournal.com'


def test_email_certificate_raises_exception(
        db_with_data: Session,
        smtp_instance
):
    quiz_service = QuizService(db_with_data)
    smtp_instance.send_message.side_effect = ValueError('something went wrong')
    with pytest.raises(SendEmailError):
        quiz_service.email_certificate('Test_User', 'Travel Training for Ministry of Magic', 'test_user@freemanjournal.com', b'')
