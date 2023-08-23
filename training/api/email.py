from string import Template
from pydantic import EmailStr
from smtplib import SMTP
from email.message import EmailMessage

from training.config import settings
from training.errors import SendEmailError

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
email us at gsa_smartpay@gsa.gov.
</p>
<p>Thank you.</p>
''')


def send_email(to_email: EmailStr, name: str, link: str, training_title: str) -> None:

    if training_title and "certificate" in training_title.lower():
        subject = "GSA SmartPayⓇ training certificate(s)"
        email_subject = "Access your GSA SmartPay training certificate(s)"
    elif training_title and "report" in training_title.lower():
        subject = "GSA SmartPayⓇ reporting information for A/OPCs"
        email_subject = "Access to GSA SmartPay training report"
    else:
        subject = f"GSA SmartPayⓇ {training_title} quiz"
        email_subject = f"Access GSA SmartPay {training_title} quiz"

    body = EMAIL_TEMPLATE.substitute({"name": name, "link": link, "subject": subject})
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
