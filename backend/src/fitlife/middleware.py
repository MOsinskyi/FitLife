import time
from collections.abc import Callable

from fastapi import Request


async def process_time_middleware(request: Request, call_next: Callable):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.5f} seconds"
    return response
