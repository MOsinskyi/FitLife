import hashlib
from collections.abc import Callable
from typing import Any

from starlette.requests import Request
from starlette.responses import Response

from fitlife.coaches.services import CoachService
from fitlife.members.services import MemberService
from fitlife.training_sessions.services import TrainingSessionService


def custom_key_builder(  # noqa: PLR0913
    func: Callable[..., Any],
    namespace: str,
    *,
    request: Request | None = None,
    response: Response | None = None,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> str:
    exclude_types = (
        MemberService,
        CoachService,
        TrainingSessionService,
    )
    new_kw = {}
    for key, value in kwargs.items():
        if isinstance(value, exclude_types):
            continue
        new_kw[key] = value
    cache_key = hashlib.md5(  # noqa: S324
        f"{func.__module__}:{func.__name__}:{args}:{new_kw}".encode()
    ).hexdigest()
    return f"{namespace}:{cache_key}"
