from typing import Annotated, Any

from pydantic import AfterValidator, BaseModel
from pydantic_settings import BaseSettings

from fitlife import constants


def is_not_none(value: Any) -> Any:
    if value is None:
        return ValueError('Value cannot be None')
    return value


class AppConfig(BaseSettings):
    title: Annotated[str, AfterValidator(is_not_none)] = constants.APP_TITLE
    api_v1: Annotated[str, AfterValidator(is_not_none)] = constants.API_V1_STR


class SqliteConfig(BaseModel):
    url: str = 'sqlite+aiosqlite:///fitlife.sqlite3'


class RedisDB(BaseModel):
    cache: int = 0


class RedisConfig(BaseModel):
    host: Annotated[str, AfterValidator(is_not_none)] = constants.REDIS_HOST
    port: Annotated[int, AfterValidator(is_not_none)] = constants.REDIS_PORT
    db: RedisDB = RedisDB()


class CacheNamespace(BaseModel):
    member: str = 'member'
    coach: str = 'coach'


class CacheConfig(BaseModel):
    prefix: Annotated[str, AfterValidator(is_not_none)] = constants.CACHE_PREFIX
    namespace: CacheNamespace = CacheNamespace()


class Settings(BaseSettings):
    app: AppConfig = AppConfig()
    redis: RedisConfig = RedisConfig()
    cache: CacheConfig = CacheConfig()
    database: SqliteConfig = SqliteConfig()


settings = Settings()
