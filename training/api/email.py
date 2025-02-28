from itertools import islice
import logging
from string import Template
from typing import Iterator, List, NamedTuple
import uuid
from pydantic import EmailStr
from smtplib import SMTP
from email.message import EmailMessage

from training.config import settings, Settings
from training.errors import SendEmailError
import time

# We also use jinja template.
# See: https://sabuhish.github.io/fastapi-mail/example/#using-jinja2-html-templates

EMAIL_TEMPLATE = Template('''
<p>Hello $name,</p>

<p>
Click the link below to access your $subject.
</p>
<p><a href="$link">$link</a></p>
<p>This link will expire in 24 hours.</p>
<p>
If you did not submit this request, you may be receiving this message in error.
Please disregard this email. If you have any questions or need further assistance,
email us at <a href="mailto:$mailto">$mailto</a>.
</p>
<p>Thank you.</p>
''')

GSPC_INVITE_EMAIL_TEMPLATE = Template('''
<p>Greetings!</p>

<p>
During the GSA SmartPay® Training Forum, you completed the required coursework for the GSA SmartPay Program Certification (GSPC)
 defined by <a href="https://smartpay.gsa.gov/policies-and-audits/smart-bulletins/022/">Smart Bulletin 22</a>.
</p>
<p>
GSPC recipients are also required to have a minimum of six (6) months of continuous, hands-on experience working with the GSA SmartPay program.
</p>
<p>
Please do not share this link with others.
</p>

<p><a href="$link">$link</a></p>

<p>
After completing this action, your GSPC will be immediately emailed to you and available for download within the training system.
If you have any questions or need further assistance, email us at <a href="mailto:gsa_smartpay@gsa.gov">gsa_smartpay@gsa.gov</a>.
</p>
<p>Thank you.</p>
''')


# Todo move email function from quiz.py and turn this into a service so that it can be mocked
def send_email(to_email: EmailStr, name: str, link: str, training_title: str) -> None:
    # Todo clean this up
    mailto = "gsa_smartpay@gsa.gov"

    if training_title and "certificate" in training_title.lower():
        subject = "GSA SmartPay® training certificate(s)"
        email_subject = "Access your GSA SmartPay training certificate(s)"
    elif training_title and "report" in training_title.lower():
        subject = "GSA SmartPay® reporting information for A/OPCs"
        email_subject = "Access to GSA SmartPay training report"
    elif training_title and "gspc_registration" in training_title.lower():
        subject = "GSA SmartPay® GSPC Registration form"
        email_subject = "Access to GSA SmartPay GSPC Registration"
        mailto = "smartpaygspc@gsa.gov"
    else:
        subject = f"GSA SmartPay® {training_title} quiz"
        email_subject = f"Access GSA SmartPay {training_title} quiz"

    body = EMAIL_TEMPLATE.substitute({"name": name, "link": link, "subject": subject, "mailto": mailto})
    message = EmailMessage()
    message.set_content(body, subtype="html")
    message["Subject"] = email_subject
    message["From"] = f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM}>"
    message["To"] = to_email

    with SMTP(settings.SMTP_SERVER, port=settings.SMTP_PORT) as smtp:
        smtp.starttls()
        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            smtp.login(user=settings.SMTP_USER, password=settings.SMTP_PASSWORD)
        try:
            smtp.send_message(message)
        except Exception as e:
            raise SendEmailError from e
        finally:
            smtp.quit()


def send_gspc_invite_email(to_email: EmailStr, link: str) -> None:
    body = GSPC_INVITE_EMAIL_TEMPLATE.substitute({"link": link})
    message = EmailMessage()
    message.set_content(body, subtype="html")
    message["Subject"] = "Verify your GSA SmartPay Program Certification (GSPC) Coursework and Experience"
    message["From"] = f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM}>"
    message["To"] = to_email

    with SMTP(settings.SMTP_SERVER, port=settings.SMTP_PORT) as smtp:
        smtp.starttls()
        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            smtp.login(user=settings.SMTP_USER, password=settings.SMTP_PASSWORD)
        try:
            smtp.send_message(message)
        except Exception as e:
            raise SendEmailError from e
        finally:
            smtp.quit()


class InviteTuple(NamedTuple):
    gspc_invite_id: uuid.UUID
    email: str


def send_gspc_invite_emails(invites: list[InviteTuple], app_settings: Settings) -> None:
    """Background task designed to do a bulk send of GSPC invite emails"""
    # Start timer to track how long the job takes
    start_time = time.time()
    logging.info(f"Starting gspc invite job, number of invites:{len(invites)}")

    email_messages = [create_email_message(invite, app_settings) for invite in invites]
    send_emails_in_batches(email_messages=email_messages, batch_size=25, app_settings=app_settings)

    end_time = time.time()
    execution_time = end_time - start_time
    # Format time as minutes and seconds for better readability
    minutes = int(execution_time // 60)
    seconds = int(execution_time % 60)
    logging.info(f"Finished gspc invite job. Total execution time: {minutes} minutes and {seconds} seconds for {len(invites)} emails")


def create_email_message(invite: InviteTuple, app_settings: Settings) -> EmailMessage:
    """Create an EmailMessage object for a given invite."""

    link = f"{app_settings.BASE_URL}/gspc_registration/?gspcInviteId={invite.gspc_invite_id}"
    body = GSPC_INVITE_EMAIL_TEMPLATE.substitute({"link": link})

    message = EmailMessage()
    message.set_content(body, subtype="html")
    message["Subject"] = "Verify your GSA SmartPay Program Certification (GSPC) Coursework and Experience"
    message["From"] = f"{app_settings.EMAIL_FROM_NAME} <{app_settings.EMAIL_FROM}>"
    message["To"] = invite.email

    return message


def batch_iterator(items: List, batch_size: int) -> Iterator:
    """Create an iterator that yields batches of the specified size."""
    iterator = iter(items)
    batch = list(islice(iterator, batch_size))
    while batch:
        yield batch
        batch = list(islice(iterator, batch_size))


def send_emails_in_batches(email_messages: List[EmailMessage], batch_size: int, app_settings: Settings) -> None:
    """Chunks the list into batches and attempts to send each back of emails."""
    for batch in batch_iterator(email_messages, batch_size):
        max_retries = 3
        # Attempt to trigger email batch, retries on failure
        for attempt in range(max_retries):
            try:
                with SMTP(app_settings.SMTP_SERVER, port=app_settings.SMTP_PORT, timeout=30) as smtp:
                    smtp.starttls()
                    if app_settings.SMTP_USER and app_settings.SMTP_PASSWORD:
                        smtp.login(user=app_settings.SMTP_USER, password=app_settings.SMTP_PASSWORD)

                    # Send messages in current batch
                    for message in batch:
                        smtp.send_message(message)
                    smtp.quit()
                break  # Exit retry loop if successful
            except Exception as e:
                if attempt < max_retries - 1:
                    # Wait with backoff: 1, 2, 4 seconds...
                    sleep_time = 1 * (attempt + 1)
                    time.sleep(sleep_time)
                # Log the error after all retries failed
                else:
                    # Extract all email addresses from the batch and join them with commas
                    addresses_list = ", ".join([message['To'] for message in batch])
                    logging.error(f"Failed to send batch after {max_retries} attempts: {str(e)}. Addresses: {addresses_list}")
