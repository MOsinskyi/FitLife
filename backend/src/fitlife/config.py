from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Gym Training Network API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = NotImplemented  # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DATABASE_URL: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
