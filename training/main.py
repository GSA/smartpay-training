from fastapi import FastAPI
from training.config import settings
from training.api.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME
)

app.include_router(api_router, prefix=settings.API_V1_STR)
