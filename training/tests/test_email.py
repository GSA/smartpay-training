import pytest
from unittest.mock import patch

from training.api import email
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
