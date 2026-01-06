from coverage.collector import os
from dotenv import load_dotenv

load_dotenv()

ALLOW_ORIGINS: list[str] = os.getenv('ALLOW_ORIGINS', '*')
ALLOW_METHODS: list[str] = os.getenv('ALLOW_METHODS', '*')
ALLOW_HEADERS: list[str] = os.getenv('ALLOW_HEADERS', '*')
ALLOW_CREDENTIALS: bool = bool(os.getenv('ALLOW_CREDENTIALS', True))

APP_NAME: str = os.getenv('APP_NAME', 'FastAPI')
VERSION: str = os.getenv('VERSION', '1.0.0')
API_V1_STR: str = os.getenv('API_V1_STR', '/api/v1')

CACHE_PREFIX: str = os.getenv('CACHE_PREFIX', 'cache')
REDIS_HOST: str = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT: int = int(os.getenv('REDIS_PORT', 6379))
