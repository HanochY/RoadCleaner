
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from uuid import uuid4, UUID
from sqlalchemy.dialects.postgresql import UUID as SQL_UUID

class Base(DeclarativeBase):
    pass

class Common(Base):
    __abstract__ = True
    
    id: Mapped[UUID] = mapped_column(SQL_UUID(as_uuid=True), default=uuid4, primary_key=True)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    created_by: Mapped[str]
    modified_at: Mapped[datetime] = mapped_column(default=datetime.now)
    modified_by: Mapped[str]
    deleted_at: Mapped[datetime | None] = mapped_column(default=None)
    deleted_by: Mapped[str | None] = mapped_column(default=None)

