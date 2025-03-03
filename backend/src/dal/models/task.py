from dal.models._base import Common
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4, UUID
from sqlalchemy.dialects.postgresql import UUID as SQL_UUID
from datetime import datetime
from sqlalchemy import ForeignKey

class Task(Common):
    __tablename__ = 'task'
    
    name: Mapped[str]
    subject: Mapped[UUID]
    start_time: Mapped[datetime] = mapped_column(default=datetime.now)
    end_time: Mapped[datetime | None] = mapped_column(default=None)
    tunnel_id: Mapped[UUID | None] = mapped_column(ForeignKey("tunnel.id"), name="tunnel")
    
    tunnel: Mapped["Tunnel"] = relationship(back_populates="tasks") # type: ignore
