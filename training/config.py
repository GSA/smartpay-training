from pydantic import BaseSettings, EmailStr
from typing import Dict, Any
from cfenv import AppEnv


def vcap_services_settings(settings: BaseSettings) -> Dict[str, Any]:
    '''
    Parse settings from the VCAP_SERVICES environment variable.
    '''
    appenv = AppEnv()
    config = {}

    redis = appenv.get_service(label="aws-elasticache-redis")
    if redis:
        config["REDIS_HOST"] = redis.credentials["host"]
        config["REDIS_PORT"] = redis.credentials["port"]
        config["REDIS_PASSWORD"] = redis.credentials["password"]

    secrets = appenv.get_service(label="user-provided")
    if secrets and secrets.credentials["JWT_SECRET"]:
        config["JWT_SECRET"] = secrets.credentials["JWT_SECRET"]
    if secrets and secrets.credentials["SMTP_PASSWORD"]:
        config["SMTP_PASSWORD"] = secrets.credentials["SMTP_PASSWORD"]

    return config


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
    EMAIL_FROM: EmailStr
    EMAIL_FROM_NAME: str
    EMAIL_SUBJECT: str
    SMTP_STARTTLS: bool
    SMTP_SSL_TLS: bool

    # These are normally parsed from VCAP_SERVICES in Cloud Foundry, but can
    # be overridden locally by using the .env file.
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            return (
                init_settings,
                env_settings,
                file_secret_settings,
                vcap_services_settings,
            )


settings = Settings()  # type: ignore
