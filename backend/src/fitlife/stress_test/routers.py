import time

from fastapi import APIRouter, status

from fitlife.database import RedisDep
from fitlife.schemas import OkResponse
from fitlife.stress_test.schemas import HealthyResponse

router = APIRouter()


@router.get(
    '/health/check',
    summary='Do health check',
    tags=['♥️ Healthy'],
    description='Check health status of backend',
    responses={
        status.HTTP_200_OK: {
            'model': HealthyResponse,
            'description': 'Healthy',
        }
    },
)
async def health_check():
    return HealthyResponse()


@router.post(
    '/heavy-calculation',
    summary='Do stress test',
    tags=['🪛 Test'],
    description='Simulate heavy calculation',
    responses={
        status.HTTP_200_OK: {
            'model': OkResponse,
            'description': 'OK',
        }
    },
)
async def stress_test(cache: RedisDep, iterations: int = 10000000, chars_count: int = 25):

    start_time = time.perf_counter()

    value = cache.get(f'stress_test_{iterations}_{chars_count}')

    if value is None:
        calculation = str([i**2 for i in range(iterations)])
        value = f'...{calculation[len(calculation) - chars_count :]}'
        cache.setex(f'stress_test_{iterations}_{chars_count}', 120, value)

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time

    return OkResponse(msg=f'{value}, elapsed job time: {elapsed_time:.4} seconds')
