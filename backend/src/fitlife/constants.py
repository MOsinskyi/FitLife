from coverage.collector import os
from dotenv import load_dotenv

load_dotenv()

ALLOW_ORIGINS: list[str] = os.getenv('ALLOW_ORIGINS', '*')
ALLOW_METHODS: list[str] = os.getenv('ALLOW_METHODS', '*')
ALLOW_HEADERS: list[str] = os.getenv('ALLOW_HEADERS', '*')
ALLOW_CREDENTIALS: bool = bool(os.getenv('ALLOW_CREDENTIALS', True))

APP_TITLE: str = os.getenv('APP_TITLE', 'FastAPI')
VERSION: str = os.getenv('VERSION', '1.0.0')
API_V1_STR: str = os.getenv('API_V1_STR', '/api/v1')
APP_HOST: str = os.getenv('APP_HOST', 'localhost')
APP_PORT: int = int(os.getenv('APP_PORT', '8000'))
LOG_FILE_NAME: str = os.getenv('LOG_FILE_NAME', 'fitlife.log')

if not LOG_FILE_NAME.endswith('.log'):
    LOG_FILE_NAME += '.log'

CACHE_PREFIX: str = os.getenv('CACHE_PREFIX', 'cache')
REDIS_HOST: str = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT: int = int(os.getenv('REDIS_PORT', 6379))
