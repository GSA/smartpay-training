from typing import Tuple, Type
from pydantic import EmailStr
from typing import Dict, Any
from cfenv import AppEnv
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict


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
        config["REDIS_TLS"] = True  # cloud.gov Redis always requires TLS

    db = appenv.get_service(label="aws-rds")
    if db:
        config["DB_URI"] = db.credentials["uri"]

    secrets = appenv.get_service(label="user-provided")
    if secrets and secrets.credentials["JWT_SECRET"]:
        config["JWT_SECRET"] = secrets.credentials["JWT_SECRET"]
    if secrets and secrets.credentials.get("SMTP_PASSWORD", None):
        config["SMTP_PASSWORD"] = secrets.credentials["SMTP_PASSWORD"]

    idp = appenv.get_service(label="cloud-gov-identity-provider")
    if idp and idp.credentials["client_id"]:
        config["AUTH_CLIENT_ID"] = idp.credentials["client_id"]

    return config


class Settings(BaseSettings):
    '''
    App-wide configurations. Where values are not provided this will attempt
    to use evnironmental variables or look in an `.env` file in the main directory.
    '''
    JWT_SECRET: str
    PROJECT_NAME: str = "GSA SmartPay Training"
    # url for front end
    BASE_URL: str
    # Number of seconds user has to click email link
    EMAIL_TOKEN_TTL: int = 60 * 60 * 24

    API_V1_STR: str = "/api/v1"

    LOG_LEVEL: str = "INFO"

    # for local dev, email setting should be added to .env
    # see .env_example for example
    SMTP_USER: str | None = None
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_STARTTLS: bool | None = None
    SMTP_SSL_TLS: bool | None = None

    EMAIL_FROM: EmailStr = "smartpay-noreply@gsa.gov"
    EMAIL_FROM_NAME: str = "GSA SmartPay"
    EMAIL_SUBJECT: str = "GSA SmartPay Training"

    # These are normally parsed from VCAP_SERVICES in Cloud Foundry, but can
    # be overridden locally by using the .env file.
    SMTP_PASSWORD: str | None = None
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_TLS: bool = False
    DB_URI: str

    # Authentication settings. The client ID is normally parsed from
    # VCAP_SERVICES in Cloud Foundry. The authority URL should be set in the
    # environment or the .env file.
    AUTH_CLIENT_ID: str
    AUTH_AUTHORITY_URL: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

    @classmethod
    def customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            file_secret_settings,
            vcap_services_settings,
        )


settings = Settings()  # type: ignore
