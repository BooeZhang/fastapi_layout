from fastapi import FastAPI, APIRouter

from rest.common import index, login


def register_api_routes(app: FastAPI):
    api_router = APIRouter(prefix="/api")
    api_router.include_router(index.router)
    api_router.include_router(login.router)

    app.include_router(router=api_router)
