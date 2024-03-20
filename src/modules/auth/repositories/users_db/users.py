from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.modules.auth.schemas.users import UserToCreate
from .base_repository import ORMRepository
from src.modules.auth.models.users import UserModel


class UserRepository(ORMRepository):
    model = UserModel

    async def create_user(
        self,
        async_session_maker: async_sessionmaker[AsyncSession],
        user_data: UserToCreate,
    ) -> UserModel:
        async with async_session_maker() as session:
            new_user = UserModel(
                phone_number=user_data.phone_number,
                role=user_data.role,
                hashed_password=user_data.hashed_password,
            )
            await self._create_one(session, new_user)
            return new_user

    async def get_user_by_phone_number(
        self,
        async_session_maker: async_sessionmaker[AsyncSession],
        phone_number: str,
    ) -> UserModel | None:
        async with async_session_maker() as session:
            stmt = select(self.model).where(UserModel.phone_number == phone_number)
            result = await session.execute(stmt)
            return result.scalars().one_or_none()

    # async def get_all_landings(self) -> List[LandingDTO]:
    #     return [
    #         LandingDTO.model_validate(
    #             obj=item,
    #             from_attributes=True
    #         ) for item in await self.raw_get_all()
    #     ]
