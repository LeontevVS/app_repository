from sqlalchemy.ext.asyncio import async_sessionmaker

from schemas.users import UserToCreate
from .base_repository import ORMRepository
from models.users import UserModel


class UserRepository(ORMRepository):
    model = UserModel

    async def create_user(
        self,
        async_session_maker: async_sessionmaker,
        user_data: UserToCreate,
    ) -> UserModel:
        new_user = UserModel(
            phone_number=user_data.phone_number,
            role=user_data.role,
            hashed_password=user_data.password,
        )
        await self._create_one(async_session_maker, new_user)
        return new_user

    # async def get_all_landings(self) -> List[LandingDTO]:
    #     return [
    #         LandingDTO.model_validate(
    #             obj=item,
    #             from_attributes=True
    #         ) for item in await self.raw_get_all()
    #     ]
