from fastapi import APIRouter, status

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
async def stress_test(iterations: int = 10000000, chars_count: int = 25):
    calculation = str([i**2 for i in range(iterations)])
    return OkResponse(msg=f'...{calculation[len(calculation) - chars_count :]}')
