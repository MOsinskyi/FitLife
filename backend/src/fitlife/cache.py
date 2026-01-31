import hashlib
from collections.abc import Callable
from typing import Any

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis
from starlette.requests import Request
from starlette.responses import Response

from fitlife.config import settings
from fitlife.member.dependencies import MemberServiceDep


async def init_cache():
    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db,
    )

    FastAPICache.init(
        RedisBackend(redis),
        prefix=settings.cache.prefix,
    )


def custom_key_builder(  # noqa: PLR0913
    func: Callable[..., Any],
    namespace: str,
    *,
    request: Request | None = None,
    response: Response | None = None,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> str:
    exclude_types = (MemberServiceDep,)
    new_kw = {}
    for key, value in kwargs.items():
        if isinstance(value, exclude_types):
            continue
        new_kw[key] = value
    cache_key = hashlib.md5(  # noqa: S324
        f'{func.__module__}:{func.__name__}:{args}:{new_kw}'.encode()
    ).hexdigest()
    return f'{namespace}:{cache_key}'
