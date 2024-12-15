from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from modules.users.consts import PrivateUserRoles
from utils_backend.sql_alchemy.base_model import ORMBaseTableModel


class UserTableModel(ORMBaseTableModel):
    __tablename__ = "users"

    user_id: Mapped[UUID] = mapped_column(primary_key=True, server_default=text("gen_random_uuid()"))
    role: Mapped[PrivateUserRoles] = mapped_column(nullable=False)
