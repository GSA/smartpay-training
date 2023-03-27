from string import Template
from pydantic import EmailStr
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
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

conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.EMAIL_FROM,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_FROM_NAME=settings.EMAIL_FROM_NAME,
    MAIL_SERVER=settings.SMTP_SERVER,
    MAIL_STARTTLS=settings.SMTP_STARTTLS,
    MAIL_SSL_TLS=settings.SMTP_SSL_TLS,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def send_email(to_email: EmailStr, name: str, link: str, training_title: str) -> JSONResponse:
    body = EMAIL_TEMPLATE.substitute({"name": name, "link": link, "training_title": training_title})

    message = MessageSchema(
        subject=settings.EMAIL_SUBJECT,
        recipients=[to_email],
        body=body,
        subtype=MessageType.html,
    )
    fm = FastMail(conf)
    await fm.send_message(message)

    return JSONResponse(status_code=200, content={"message": "email sent"})
