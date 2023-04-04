from fastapi import APIRouter

from training.api.api_v1 import loginless_flow, agencies, users, quizzes

api_router = APIRouter()

api_router.include_router(loginless_flow.router)
api_router.include_router(agencies.router)
api_router.include_router(users.router)
api_router.include_router(quizzes.router)
