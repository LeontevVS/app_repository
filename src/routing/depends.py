from repositories.landings import LandingRepository
from services.landings import LandingService


# repositories
landing_repository = LandingRepository()

# services
landing_service = LandingService(landing_repository)


def get_landing_service() -> LandingService:
    return landing_service
