from typing import TYPE_CHECKING
from fitlife.passes.models import PassModel

if TYPE_CHECKING:
    from .repositories import PassRepository, PassFeatureRepository

class PassService:
    def __init__(self, repository: "PassRepository", feature_repository: "PassFeatureRepository"):
        self._repository = repository
        self._feature_repository = feature_repository

    async def get_active_passes(self) -> list[PassModel]:
        return await self._repository.get_all_active()
