from typing import Any

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


def is_not_none(value: Any) -> Any:
    if value is None:
        return ValueError('Value cannot be None')
    return value


class AppConfig(BaseModel):
    name: str = 'FastAPI'
    api_v1: str = '/api/v1'
    host: str = 'localhost'
    port: int = 8000
    log_filename: str = 'fitlife.log'
    version: str = '0.1.0'


class SecurityConfig(BaseModel):
    secret_key: str = 'xxx'
    algorithm: str = 'xxx'
    access_token_expire_minutes: int = 30
    hash_encoding: str = 'utf-8'


class MiddlewareConfig(BaseModel):
    allow_origins: list[str] | str = '*'
    allow_methods: list[str] | str = '*'
    allow_headers: list[str] | str = '*'
    allow_credentials: bool = True


class SqliteConfig(BaseModel):
    url: str = 'sqlite+aiosqlite:///fitlife.sqlite3'


class RedisDB(BaseModel):
    cache: int = 0


class RedisConfig(BaseModel):
    host: str = 'localhost'
    port: int = 6379
    db: RedisDB = RedisDB()


class CacheNamespace(BaseModel):
    member: str = 'member'
    coach: str = 'coach'
    training_session: str = 'training_session'


class CacheConfig(BaseModel):
    prefix: str = 'fitlife'
    namespace: CacheNamespace = CacheNamespace()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_ignore_empty=True,
        env_nested_delimiter='_',
        env_nested_max_split=1,
    )

    app: AppConfig = AppConfig()
    middleware: MiddlewareConfig = MiddlewareConfig()
    redis: RedisConfig = RedisConfig()
    cache: CacheConfig = CacheConfig()
    database: SqliteConfig = SqliteConfig()
    security: SecurityConfig = SecurityConfig()


settings = Settings()
