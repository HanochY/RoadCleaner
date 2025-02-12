
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Common(Base):
    __abstract__ = True
    
    is_deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    created_by: Mapped[str]
    modified_at: Mapped[datetime] = mapped_column(default=datetime.now)
    modified_by: Mapped[str]
    deleted_at: Mapped[datetime | None] = mapped_column(default=None)
    deleted_by: Mapped[str | None] = mapped_column(default=None)

