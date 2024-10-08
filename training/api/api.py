from fastapi import APIRouter

from training.api.api_v1 import auth, loginless_flow, agencies, users, quizzes, certificates, gspc

api_router = APIRouter()

api_router.include_router(agencies.router)
api_router.include_router(auth.router)
api_router.include_router(certificates.router)
api_router.include_router(gspc.router)
api_router.include_router(loginless_flow.router)
api_router.include_router(quizzes.router)
api_router.include_router(users.router)
