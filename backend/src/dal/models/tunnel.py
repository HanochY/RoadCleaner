from dal.models._base import Common
from sqlalchemy.orm import Mapped, relationship, mapped_column
from uuid import uuid4, UUID
from sqlalchemy.dialects.postgresql import UUID as SQL_UUID
from datetime import datetime
class Tunnel(Common):
    __tablename__ = 'tunnel'
    
    unique_name: Mapped[str] = mapped_column(SQL_UUID(as_uuid=True) primary_key=True) #change this name
    name: Mapped[str]
    interfaces: Mapped[list["Interface"]] = relationship(back_populates="device") # type: ignore
    reinforced_at: Mapped[datetime | None] = mapped_column(default=None) #change this name
    reinforced_by: Mapped[str | None] = mapped_column(default=None) #change this name
