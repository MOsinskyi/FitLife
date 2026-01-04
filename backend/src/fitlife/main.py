from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis

from fitlife.config import settings
from fitlife.database import router as database_router
from fitlife.member.routers import router as member_router
from fitlife.membership.routers import router as membership_router
from fitlife.schemas import OkResponse
from fitlife.stress_test.routers import router as stress_test_router
from fitlife.trainer.routers import router as trainer_router
from fitlife.workout_session.routers import router as workout_session_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db.cache,
    )
    FastAPICache.init(
        RedisBackend(redis),
        prefix=settings.cache.prefix,
    )
    yield


app = FastAPI(
    title=settings.app.name,
    lifespan=lifespan,
    root_path=settings.app.api_v1,
    root_path_in_servers=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_credentials=True,
    allow_headers=['*'],
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
async def home():
    return OkResponse(msg="Server's working")


app.include_router(member_router)
app.include_router(trainer_router)
app.include_router(membership_router)
app.include_router(workout_session_router)
app.include_router(database_router)
app.include_router(stress_test_router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
