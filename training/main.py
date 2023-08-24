import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from training.config import settings
from training.api.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME
)
origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:3000",
    "https://localhost:3000",
    "http://127.0.0.1:3000",
    "https://training.smartpay.gov",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r'https://federalist.*\.sites\.pages\.cloud\.gov',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(levelname)s: %(module)s.%(funcName)s:%(lineno)d: %(message)s"
)
