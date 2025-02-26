from dal.models._base import Common
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4, UUID
from sqlalchemy.dialects.postgresql import UUID as SQL_UUID
from datetime import datetime

class Task(Common):
    __tablename__ = 'task'
    
    id: Mapped[UUID] = mapped_column(SQL_UUID(as_uuid=True), default=uuid4, primary_key=True)
    name: Mapped[str]
    subject: Mapped[UUID]
    start_time: Mapped[datetime] = mapped_column(default=datetime.now)
    end_time: Mapped[datetime | None] = mapped_column(default=None)
