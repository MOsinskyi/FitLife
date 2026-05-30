import os
from typing import Any

from pydantic import AliasChoices, BaseModel, Field, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def is_not_none(value: Any) -> Any:
    if value is None:
        return ValueError("Value cannot be None")
    return value


class AppConfig(BaseModel):
    name: str = "FastAPI"
    api_v1: str = Field("/api/v1", validation_alias=AliasChoices("api_v1", "api_v1_str"))
    host: str = "localhost"
    port: int = 8000
    log_filename: str = Field(
        "fitlife.log", validation_alias=AliasChoices("log_filename", "log_file_name")
    )
    version: str = "0.1.0"


class SecurityConfig(BaseModel):
    secret_key: str = "xxx"
    algorithm: str = "xxx"
    access_token_expire_minutes: int = 30
    hash_encoding: str = "utf-8"


class MiddlewareConfig(BaseModel):
    allow_origins: list[str] | str = ["*"]
    allow_methods: list[str] | str = ["*"]
    allow_headers: list[str] | str = ["*"]
    allow_credentials: bool | str = True

    @field_validator("allow_origins", "allow_methods", "allow_headers", mode="before")
    @classmethod
    def assemble_list(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            if v.strip().startswith("["):
                import json
                try:
                    return json.loads(v)
                except (json.JSONDecodeError, TypeError):
                    pass
            return [i.strip() for i in v.split(",")]
        return v

    @field_validator("allow_credentials", mode="before")
    @classmethod
    def assemble_bool(cls, v: Any) -> bool:
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes", "on")
        return bool(v)


class PostgresConfig(BaseModel):
    user: str = "postgres"
    password: str = ""
    db: str = "fitlife"
    host: str = "localhost"
    port: int = 5432

    @computed_field
    @property
    def effective_host(self) -> str:
        if self.host == "db" and not os.path.exists("/.dockerenv"):
            return "localhost"
        if self.host == "localhost" and os.path.exists("/.dockerenv"):
            return "db"
        return self.host

    @computed_field
    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.effective_host}:{self.port}/{self.db}"


class RedisDB(BaseModel):
    cache: int = 0


class RedisConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: RedisDB = RedisDB()

    @computed_field
    @property
    def effective_host(self) -> str:
        if self.host == "redis" and not os.path.exists("/.dockerenv"):
            return "localhost"
        if self.host == "localhost" and os.path.exists("/.dockerenv"):
            return "redis"
        return self.host


class CacheNamespace(BaseModel):
    member: str = "member"
    coach: str = "coach"
    training_session: str = "training_session"


class CacheConfig(BaseModel):
    prefix: str = "fitlife"
    namespace: CacheNamespace = CacheNamespace()


class AdminConfig(BaseModel):
    title: str = "FitLife Admin"
    enabled: bool = True


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env.dev",
        env_ignore_empty=True,
        env_nested_delimiter="_",
        env_nested_max_split=1,
    )

    app: AppConfig = AppConfig()
    middleware: MiddlewareConfig = MiddlewareConfig()
    redis: RedisConfig = RedisConfig()
    cache: CacheConfig = CacheConfig()
    postgres: PostgresConfig = PostgresConfig()
    security: SecurityConfig = SecurityConfig()
    admin: AdminConfig = AdminConfig()


settings = Settings()
