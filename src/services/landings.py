from datetime import datetime, timedelta
from typing import List

from repositories.landings import LandingRepository
from schemas.landings import LandingDTO


class LandingService:

    def __init__(self, repository: LandingRepository):
        self.repository = repository

    async def get_all_landings(self) -> List[LandingDTO]:
        landings = await self.repository.get_all_landings()
        published_landings = []
        not_published_landings = []
        for landing in sorted(landings, key=lambda item: item.id, reverse=True):
            landing.update_time = (
                    datetime.utcfromtimestamp(landing.update_time) + timedelta(hours=3)
            ).strftime('%d.%m.%Y %H:%M')
            published_landings.append(landing) if landing.active else not_published_landings.append(landing)
        return published_landings + not_published_landings
