from datetime import datetime, UTC

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class ORMBaseTableModel(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(insert_default=lambda: datetime.now(UTC).replace(tzinfo=None))
    deleted_at: Mapped[datetime] = mapped_column(nullable=True, default=None)
    deleted: Mapped[bool] = mapped_column(nullable=True, default=False)
