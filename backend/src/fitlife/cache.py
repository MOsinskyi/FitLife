from fastapi import BackgroundTasks
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis

from fitlife.config import settings


async def init_cache():
    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db.cache,
    )

    FastAPICache.init(
        RedisBackend(redis),
        prefix=settings.cache.prefix,
    )


async def clear_cache(background_tasks: BackgroundTasks, namespace: str):
    background_tasks.add_task(
        FastAPICache.clear,
        namespace=namespace,
    )
