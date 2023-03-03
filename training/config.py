from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    '''
    App-wide configurations. Where values are not provided this will attempt
    to use evnironmental variables or look in an `.env` file in the main directory.
    '''
    JWT_SECRET: str
    PROJECT_NAME: str = "GSA SmartPay Training"
    # url for front end
    BASE_URL: str = "http://127.0.0.1:5173"
    # Number of seconds user has to click email link
    EMAIL_TOKEN_TTL: int = 60 * 60 * 2

    API_V1_STR: str = "/api/v1"

    # for local dev, email setting should be added to .env
    # see .env_example for example
    SMTP_PASSWORD: str
    SMTP_USER: str
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_SENDER: str
    EMAIL_FROM: EmailStr
    EMAIL_FROM_NAME: str
    EMAIL_SUBJECT: str
    SMTP_STARTTLS: bool
    SMTP_SSL_TLS: bool

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()  # type: ignore
