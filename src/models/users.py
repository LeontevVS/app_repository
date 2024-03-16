from sqlalchemy.orm import Mapped, mapped_column

from enums.user_enums import PrivateUserRoles
from models.base_model import ORMBaseModel


class UserModel(ORMBaseModel):
    __tablename__ = 'users'

    phone_number: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[PrivateUserRoles] = mapped_column(nullable=False)
    hashed_password: Mapped[bytes] = mapped_column(nullable=False)
