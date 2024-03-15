from typing import List

from repositories.db.base_repository import ORMRepository
from repositories.db.models.landings import LandingModel
from schemas.landings import LandingDTO


class LandingRepository(ORMRepository):
    model = LandingModel

    async def get_all_landings(self) -> List[LandingDTO]:
        return [
            LandingDTO.model_validate(
                obj=item,
                from_attributes=True
            ) for item in await self.raw_get_all()
        ]
