from fastapi import APIRouter

from handler import index

api_router = APIRouter(prefix="/api")

api_router.include_router(index.router)
