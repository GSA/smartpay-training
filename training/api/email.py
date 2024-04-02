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

GSPC_INVITE_EMAIL_TEMPLATE = Template('''
<p>Greetings!</p>

<p>
During the GSA SmartPay Training Forum, you completed the required coursework for the GSA SmartPay Program Certification (GSPC)
 defined by <a href="https://smartpay.gsa.gov/policies-and-audits/smart-bulletins/022/">Smart Bulletin 22</a>.
</p>
<p>
GSPC recipients are also required to have a minimum of six (6) months of continuous, hands-on experience working with the GSA SmartPay program.
</p>
<p>
Please do not share this link with others as it is unique to you.
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
    if training_title and "certificate" in training_title.lower():
        subject = "GSA SmartPay® training certificate(s)"
        email_subject = "Access your GSA SmartPay training certificate(s)"
    elif training_title and "report" in training_title.lower():
        subject = "GSA SmartPay® reporting information for A/OPCs"
        email_subject = "Access to GSA SmartPay training report"
    else:
        subject = f"GSA SmartPay® {training_title} quiz"
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
