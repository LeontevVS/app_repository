from sqlalchemy.orm import Mapped, mapped_column

from src.modules.auth.enums.user_enums import PrivateUserRoles
from src.modules.auth.models.base_model import ORMBaseModel


class UserModel(ORMBaseModel):
    __tablename__ = 'users'

    phone_number: Mapped[str] = mapped_column(nullable=False, unique=True)
    role: Mapped[PrivateUserRoles] = mapped_column(nullable=False)
    hashed_password: Mapped[bytes] = mapped_column(nullable=False)
