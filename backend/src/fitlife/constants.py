from coverage.collector import os
from dotenv import load_dotenv

load_dotenv()

ALLOW_ORIGINS: list[str] = os.getenv('ALLOW_ORIGINS', '*')
ALLOW_METHODS: list[str] = os.getenv('ALLOW_METHODS', '*')
ALLOW_HEADERS: list[str] = os.getenv('ALLOW_HEADERS', '*')
ALLOW_CREDENTIALS: bool = bool(os.getenv('ALLOW_CREDENTIALS', True))

APP_NAME: str = os.getenv('APP_NAME', 'FastAPI')
VERSION: str = os.getenv('APP_NAME', '1.0.0')
API_V1_STR: str = os.getenv('APP_NAME', '/api/v1')

CACHE_PREFIX: str = os.getenv('APP_NAME', 'cache')
REDIS_HOST: str = os.getenv('APP_NAME', 'localhost')
REDIS_PORT: int = int(os.getenv('APP_NAME', 6379))
