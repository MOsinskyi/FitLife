import time

from pydantic import BaseModel


class HealthyResponse(BaseModel):
    status: str = 'healthy'
    timestamp: float = time.time()
