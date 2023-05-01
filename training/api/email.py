import logging
from string import Template
from pydantic import EmailStr
from smtplib import SMTP
from email.message import EmailMessage
from starlette.responses import JSONResponse

from training.config import settings

# We also use jinja template.
# See: https://sabuhish.github.io/fastapi-mail/example/#using-jinja2-html-templates
EMAIL_TEMPLATE = Template('''
<p>Hello $name,</p>

<p>
Thank you for registering for $training_title. Please confirm the email address
you submitted is correct by clicking on the link below.
</p>

<p><a href="$link">$link</a></p>

<p>This link will expire in 24 hours.</p>
<p>
If you did not register for this class, you may be receiving this message in error.
Please disregard this email. If you have any questions or need further assistance,
email us at gsa_smartpay@gsa.gov.
</p>
''')


async def send_email(to_email: EmailStr, name: str, link: str, training_title: str) -> JSONResponse:
    body = EMAIL_TEMPLATE.substitute({"name": name, "link": link, "training_title": training_title})

    message = EmailMessage()
    message.set_content(body, subtype="html")
    message["Subject"] = settings.EMAIL_SUBJECT
    message["From"] = f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM}>"
    message["To"] = to_email

    with SMTP(settings.SMTP_SERVER, port=settings.SMTP_PORT) as smtp:
        smtp.starttls()
        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            smtp.login(user=settings.SMTP_USER, password=settings.SMTP_PASSWORD)
        try:
            smtp.send_message(message)
            result = JSONResponse(status_code=200, content={"message": "email sent"})
        except Exception as e:
            logging.error("Error sending email", e)
            result = JSONResponse(status_code=500, content={"message": "error sending email"})
        finally:
            smtp.quit()

    return result
