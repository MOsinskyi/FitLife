from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from fitlife.cache import init_cache
from fitlife.coach.routers import router as coach_router
from fitlife.config import settings
from fitlife.member.routers import router as member_router
from fitlife.middleware import process_time_middleware
from fitlife.schemas import OkResponse


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_cache()
    yield


app = FastAPI(
    title=settings.app.name,
    lifespan=lifespan,
    root_path=settings.app.api_v1,
    root_path_in_servers=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.middleware.allow_origins,
    allow_methods=settings.middleware.allow_methods,
    allow_credentials=settings.middleware.allow_credentials,
    allow_headers=settings.middleware.allow_headers,
)

app.add_middleware(BaseHTTPMiddleware, dispatch=process_time_middleware)


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
async def home():
    return OkResponse(msg='Server is working')


app.include_router(member_router)
app.include_router(coach_router)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.app.host,
        port=settings.app.port,
        reload=True,
    )
