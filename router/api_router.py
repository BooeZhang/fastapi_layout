from fastapi import APIRouter

from service import index, login

api_router = APIRouter(prefix="/api")

api_router.include_router(index.router)
api_router.include_router(login.router)
