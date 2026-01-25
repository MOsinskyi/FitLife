from contextlib import asynccontextmanager

import logger as custom_logger
import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from fitlife import constants
from fitlife.config import settings
from fitlife.constants import APP_HOST, APP_PORT
from fitlife.database import router as database_router
from fitlife.member.routers import router as member_router
from fitlife.schemas import OkResponse


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger = custom_logger.logger
    yield {'logger': logger}
    del logger


app = FastAPI(
    title=settings.app.name,
    lifespan=lifespan,
    root_path=settings.app.api_v1,
    root_path_in_servers=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=constants.ALLOW_ORIGINS,
    allow_methods=constants.ALLOW_METHODS,
    allow_credentials=constants.ALLOW_CREDENTIALS,
    allow_headers=constants.ALLOW_HEADERS,
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'success': False,
            'msg': exc.detail,
        },
    )


@app.get(
    '/',
    response_model=OkResponse,
)
async def home(request: Request):
    request.state.logger.info('GET /')
    return OkResponse(msg='Server is working')


app.include_router(member_router)
app.include_router(database_router)


if __name__ == '__main__':
    uvicorn.run('main:app', host=APP_HOST, port=APP_PORT, reload=True)
