from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from fitlife import constants


async def initialize_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=constants.ALLOW_ORIGINS,
        allow_methods=constants.ALLOW_METHODS,
        allow_credentials=True,
        allow_headers=constants.ALLOW_HEADERS,
    )
