from dal.models._base import Common
from sqlalchemy.orm import Mapped, relationship, mapped_column
from uuid import uuid4, UUID
from sqlalchemy.dialects.postgresql import UUID as SQL_UUID
from sqlalchemy import ForeignKey, String
from datetime import datetime
class Tunnel(Common):
    __tablename__ = 'tunnel'
    
    id: Mapped[UUID] = mapped_column(SQL_UUID(as_uuid=True), default=uuid4, primary_key=True) 
    name: Mapped[str]
    interface_core_id: Mapped[UUID] = mapped_column(ForeignKey("tunnel.id"), name="interface_core")
    interface_edge_id: Mapped[UUID] = mapped_column(ForeignKey("tunnel.id"), name="interface_edge")
    reinforced_at: Mapped[datetime | None] = mapped_column(default=None) #change this name
    reinforced_by: Mapped[str | None] = mapped_column(default=None) #change this name
    vendor: Mapped[str] = mapped_column(String)
    
    __mapper_args__ = {
        'polymorphic_identity': 'tunnel',
        'polymorphic_on': vendor
    }
    
    interface_core: Mapped["Interface"] = relationship(back_populates="tunnel") # type: ignore
    interface_edge: Mapped["Interface"] = relationship(back_populates="tunnel") # type: ignore

