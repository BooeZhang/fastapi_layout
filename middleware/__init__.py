from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from middleware.unify_json import UnifyJson


def register_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 返回统一 json 中间件
    # app.add_middleware(UnifyJson)

