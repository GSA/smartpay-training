from string import Template
from pydantic import EmailStr
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from starlette.responses import JSONResponse

from training.config import settings

# We also use jinja template.
# See: https://sabuhish.github.io/fastapi-mail/example/#using-jinja2-html-templates
EMAIL_TEMPLATE = Template('''
Hello $name,

Please follow this link to access SmartPay Training:

$link
''')

conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.EMAIL_FROM,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_FROM_NAME=settings.EMAIL_FROM_NAME,
    MAIL_SERVER=settings.SMTP_SERVER,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def send_email(to_email: EmailStr, name: str, link: str) -> JSONResponse:
    body = EMAIL_TEMPLATE.substitute({"name": name, "link": link})

    message = MessageSchema(
        subject=settings.EMAIL_SUBJECT,
        recipients=[to_email],
        body=body,
        subtype=MessageType.html,
    )
    fm = FastMail(conf)
    await fm.send_message(message)

    return JSONResponse(status_code=200, content={"message": "email sent"})
