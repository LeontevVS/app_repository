from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from utils_backend.sql_alchemy.base_model import ORMBaseTableModel


class EmailAccessTableModel(ORMBaseTableModel):
    __tablename__ = "email_access"

    email: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(primary_key=True)
    hashed_password: Mapped[bytes] = mapped_column(nullable=False)
