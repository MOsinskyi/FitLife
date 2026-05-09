from fitlife.specializations.repositories import SpecializationRepository
from fitlife.specializations.schemas import SpecializationResponse

class SpecializationService:
    def __init__(self, repository: SpecializationRepository):
        self.repository = repository

    async def get_all_specializations(self) -> list[SpecializationResponse]:
        specializations = await self.repository.get_all()
        return [SpecializationResponse.model_validate(s) for s in specializations]
