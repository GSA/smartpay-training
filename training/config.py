from pydantic import BaseSettings


class Settings(BaseSettings):
    '''
    App-wide configurations. Where values are not provided this will attempt
    to use evnironmental variables or look in an `.env` file in the main directory.
    '''
    PROJECT_NAME: str = "GSA SmartPay Training"

    # Number of seconds user has to click email link
    EMAIL_TOKEN_TTL: int = 60 * 60 * 2

    API_V1_STR: str = "/api/v1"


settings = Settings()
