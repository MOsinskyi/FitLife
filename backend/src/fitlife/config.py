import os
from typing import Annotated, Any

from dotenv import load_dotenv
from pydantic import AfterValidator, BaseModel
from pydantic_settings import BaseSettings

load_dotenv()


def is_not_none(value: Any) -> Any:
    if value is None:
        return ValueError('Value cannot be None')
    return value


class AppConfig(BaseSettings):
    name: Annotated[str, AfterValidator(is_not_none)] = os.getenv('APP_NAME', 'FastApi')
    api_v1: Annotated[str, AfterValidator(is_not_none)] = os.getenv('API_V1_STR', '/api/v1')


class RedisDB(BaseModel):
    cache: int = 0


class RedisConfig(BaseModel):
    host: Annotated[str, AfterValidator(is_not_none)] = os.getenv('REDIS_HOST', 'localhost')
    port: Annotated[int, AfterValidator(is_not_none)] = os.getenv('REDIS_PORT', None)
    db: RedisDB = RedisDB()


class CacheNamespace(BaseModel):
    member_list: str = 'member-list'


class CacheConfig(BaseModel):
    prefix: Annotated[str, AfterValidator(is_not_none)] = os.getenv('CACHE_PREFIX', 'cache')
    namespace: CacheNamespace = CacheNamespace()


class Settings(BaseSettings):
    app: AppConfig = AppConfig()
    redis: RedisConfig = RedisConfig()
    cache: CacheConfig = CacheConfig()


settings = Settings()
