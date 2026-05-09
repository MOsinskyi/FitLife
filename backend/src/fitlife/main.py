from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware

from fitlife.admin import setup_admin
from fitlife.admin.auth import authentication_backend
from fitlife.auth.routers import auth_router
from fitlife.cache import init_cache
from fitlife.coaches.routers import coach_router
from fitlife.config import settings
from fitlife.database import engine
from fitlife.gallery.routers import gallery_router
from fitlife.members.routers import member_router
from fitlife.middleware import process_time_middleware
from fitlife.specializations.routers import specialization_router
from fitlife.training_sessions.routers import training_session_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_cache()
    yield


app = FastAPI(
    title=settings.app.name,
    lifespan=lifespan,
    root_path=settings.app.api_v1,
    version=settings.app.version,
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

app.add_middleware(SessionMiddleware, secret_key=settings.security.secret_key)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'success': False,
            'msg': exc.detail,
        },
    )


app.include_router(auth_router)
app.include_router(member_router)
app.include_router(coach_router)
app.include_router(training_session_router)
app.include_router(gallery_router)
app.include_router(specialization_router)

setup_admin(app, engine, authentication_backend)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.app.host,
        port=settings.app.port,
        reload=True,
    )
