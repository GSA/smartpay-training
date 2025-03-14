from email.message import EmailMessage
import pytest
from unittest.mock import MagicMock, patch

from training.api import email
from training.config import Settings
from training.errors import SendEmailError


@pytest.fixture
def smtp_instance():
    with patch('training.api.email.SMTP') as smtp_mock:
        with smtp_mock() as smtp:
            yield smtp


@patch.multiple(email.settings,
                SMTP_SERVER='email.example.com',
                SMTP_PORT=999,
                EMAIL_FROM='J.P.Nannetti@freemanjournal.com',
                EMAIL_FROM_NAME='Joseph Patrick Nannetti',
                SMTP_USER='Aeolus',
                SMTP_PASSWORD='cycl0ps'
                )
class TestEmail:
    def test_email_uses_config(self):
        with patch('training.api.email.SMTP') as smtp_mock:
            email.send_email('l_bloom@freemanjournal.com', 'leopold', 'http://www.example.com', 'Title')
            smtp_mock.assert_called_with('email.example.com', port=999)

    def test_email_login_credentials(self, smtp_instance):
        email.send_email('l_bloom@freemanjournal.com', 'leopold', 'http://www.example.com', 'Title')
        smtp_instance.login.called_with(user='Aeolus', password='cycl0ps')

    def test_email_calls_ttls(self, smtp_instance):
        email.send_email('l_bloom@freemanjournal.com', 'leopold', 'http://www.example.com', 'Title')
        smtp_instance.starttls.assert_called()

    def test_email_raises_on_exception(self, smtp_instance):
        smtp_instance.send_message.side_effect = ValueError('whoops')
        with pytest.raises(SendEmailError):
            email.send_email('l_bloom@freemanjournal.com', 'leopold', 'http://www.example.com', 'Title')

    def test_email_to_from(self, smtp_instance):
        email.send_email('l_bloom@freemanjournal.com', 'leopold', 'http://www.example.com', 'Access Certificates')
        args, _ = smtp_instance.send_message.call_args
        email_message = args[0]
        assert email_message['From'] == 'Joseph Patrick Nannetti <J.P.Nannetti@freemanjournal.com>'
        assert email_message['To'] == 'l_bloom@freemanjournal.com'

    def test_email_link(self, smtp_instance):
        email.send_email('l_bloom@freemanjournal.com', 'leopold', 'http://www.example.com', 'Access Certificates')
        args, _ = smtp_instance.send_message.call_args
        email_message = args[0]
        message = email_message.get_content()
        assert '<a href="http://www.example.com">http://www.example.com</a>' in message

    def test_email_certificate(self, smtp_instance):
        email.send_email('l_bloom@freemanjournal.com', 'leopold', 'http://www.example.com', 'Access Certificates')
        args, _ = smtp_instance.send_message.call_args
        email_message = args[0]
        message = email_message.get_content()
        assert 'Click the link below to access your GSA SmartPay® training certificate(s)' in message
        assert email_message['Subject'] == 'Access your GSA SmartPay training certificate(s)'

    def test_email_report(self, smtp_instance):
        email.send_email('l_bloom@freemanjournal.com', 'leopold', 'http://www.example.com', 'Training Reports')
        args, _ = smtp_instance.send_message.call_args
        email_message = args[0]
        message = email_message.get_content()
        assert 'Click the link below to access your GSA SmartPay® reporting information for A/OPCs' in message
        assert email_message['Subject'] == 'Access to GSA SmartPay training report'

    def test_email_quiz(self, smtp_instance):
        email.send_email('l_bloom@freemanjournal.com', 'leopold', 'http://www.example.com', 'Ad Sales')
        args, _ = smtp_instance.send_message.call_args
        email_message = args[0]
        message = email_message.get_content()
        assert 'Click the link below to access your GSA SmartPay® Ad Sales quiz.' in message
        assert email_message['Subject'] == 'Access GSA SmartPay Ad Sales quiz'

    def test_create_email_message(self):
        invite = email.InviteTuple(gspc_invite_id="12345", email="test@example.com", version=email.GspcEmailVersion.INITIAL)
        app_settings = Settings(BASE_URL="https://example.com", EMAIL_FROM_NAME="GSPC", EMAIL_FROM="noreply@example.com")

        message = email.create_email_message(invite, app_settings)

        assert isinstance(message, EmailMessage)
        assert message["To"] == "test@example.com"
        assert message["From"] == "GSPC <noreply@example.com>"
        assert message["Subject"] == "Verify your GSA SmartPay Program Certification (GSPC) Coursework and Experience"

    def test_create_email_message_second_notice(self):
        invite = email.InviteTuple(gspc_invite_id="12345", email="test@example.com", version=email.GspcEmailVersion.SECOND)
        app_settings = Settings(BASE_URL="https://example.com", EMAIL_FROM_NAME="GSPC", EMAIL_FROM="noreply@example.com")

        message = email.create_email_message(invite, app_settings)

        assert isinstance(message, EmailMessage)
        assert message["To"] == "test@example.com"
        assert message["From"] == "GSPC <noreply@example.com>"
        assert message["Subject"] == "Second Notification - Verify your GSA SmartPay Program Certification (GSPC) Coursework and Experience"

    def test_create_email_message_final_notice(self):
        invite = email.InviteTuple(gspc_invite_id="12345", email="test@example.com", version=email.GspcEmailVersion.FINAL)
        app_settings = Settings(BASE_URL="https://example.com", EMAIL_FROM_NAME="GSPC", EMAIL_FROM="noreply@example.com")

        message = email.create_email_message(invite, app_settings)

        assert isinstance(message, EmailMessage)
        assert message["To"] == "test@example.com"
        assert message["From"] == "GSPC <noreply@example.com>"
        assert message["Subject"] == "Final Notification - Verify your GSA SmartPay Program Certification (GSPC) Coursework and Experience"

    def test_batch_iterator_even_batches(self):
        items = [1, 2, 3, 4, 5, 6]
        batch_size = 2
        expected_batches = [[1, 2], [3, 4], [5, 6]]

        result = list(email.batch_iterator(items, batch_size))

        assert result == expected_batches

    def test_batch_iterator_uneven_batches(self):
        items = [1, 2, 3, 4, 5]
        batch_size = 2
        expected_batches = [[1, 2], [3, 4], [5]]

        result = list(email.batch_iterator(items, batch_size))

        assert result == expected_batches

    def test_batch_iterator_single_item(self):
        items = [1]
        batch_size = 2
        expected_batches = [[1]]

        result = list(email.batch_iterator(items, batch_size))

        assert result == expected_batches

    def test_batch_iterator_empty_list(self):
        items = []
        batch_size = 2
        expected_batches = []

        result = list(email.batch_iterator(items, batch_size))

        assert result == expected_batches

    def test_send_gspc_completion_email(self, smtp_instance):
        failed_emails = "test1@example.com, test2@example.com"
        app_settings = Settings(
            EMAIL_FROM_NAME="GSPC",
            EMAIL_FROM="noreply@example.com",
            GSPC_MAILBOX="gspc@example.com",
            SMTP_SERVER="smtp.example.com",
            SMTP_PORT=587,
            SMTP_USER="user",
            SMTP_PASSWORD="password"
        )

        email.send_gspc_completion_email(failed_emails, app_settings)

        smtp_instance.starttls.assert_called_once()
        smtp_instance.login.assert_called_once_with(user="user", password="password")
        smtp_instance.send_message.assert_called_once()
        smtp_instance.quit.assert_called_once()

    def test_send_gspc_invite_emails(self):
        invites = [
            email.InviteTuple(email="test1@example.com", gspc_invite_id="123", version="INITIAL"),
            email.InviteTuple(email="test2@example.com", gspc_invite_id="456", version="SECOND"),
        ]
        app_settings = Settings()

        with patch("training.api.email.create_email_message") as mock_create_email, \
             patch("training.api.email.send_emails_in_batches") as mock_send_batches, \
             patch("training.api.email.logging.info") as mock_log, \
             patch("training.api.email.time.time", side_effect=[1, 2]):  # Simulates execution time

            mock_create_email.side_effect = lambda invite, settings: f"EmailMessage for {invite.email}"

            email.send_gspc_invite_emails(invites, app_settings)

            assert mock_create_email.call_count == len(invites)
            mock_send_batches.assert_called_once_with(
                email_messages=["EmailMessage for test1@example.com", "EmailMessage for test2@example.com"],
                batch_size=25,
                app_settings=app_settings
            )

            mock_log.assert_any_call("Starting gspc invite job, number of invites:2")
            mock_log.assert_any_call("Finished gspc invite job. Total execution time: 0 minutes and 1 seconds for 2 emails")

    def test_send_emails_in_batches(self, smtp_instance):
        email_messages = [MagicMock(), MagicMock()]
        app_settings = Settings(
            SMTP_SERVER="smtp.example.com",
            SMTP_PORT=587,
            SMTP_USER="user",
            SMTP_PASSWORD="password"
        )

        with patch("training.api.email.batch_iterator", return_value=[email_messages]), \
             patch("training.api.email.logging.error"), \
             patch("training.api.email.send_gspc_completion_email") as mock_completion:

            email.send_emails_in_batches(email_messages, batch_size=25, app_settings=app_settings)

            smtp_instance.starttls.assert_called_once()
            smtp_instance.login.assert_called_once_with(user="user", password="password")
            assert smtp_instance.send_message.call_count == len(email_messages)
            smtp_instance.quit.assert_called_once()
            mock_completion.assert_called_once()
