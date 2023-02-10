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
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
