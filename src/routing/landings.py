from typing import List

from fastapi import APIRouter, Depends

from .depends import get_landing_service
from schemas.landings import LandingDTO
from services.landings import LandingService


router = APIRouter(tags=['landings'])


@router.get(
    path='/api/landings',
    response_model=List[LandingDTO],
)
async def get_all_landings(
    landing_service: LandingService = Depends(get_landing_service),
) -> List[LandingDTO]:
    return await landing_service.get_all_landings()
