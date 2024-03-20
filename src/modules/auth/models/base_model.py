import datetime

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class ORMBaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    deleted_at: Mapped[datetime.datetime] = mapped_column(nullable=True)
    is_deleted: Mapped[bool] = mapped_column(nullable=False, default=True)
