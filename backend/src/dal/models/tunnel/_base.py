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
    interface_inner_id: Mapped[UUID | None] = mapped_column(ForeignKey("interface.id"), name="interface_inner", unique=True)
    interface_outer_id: Mapped[UUID | None] = mapped_column(ForeignKey("interface.id"), name="interface_outer", unique=True) 
    reinforced_at: Mapped[datetime | None] = mapped_column(default=None) #change this name
    reinforced_by: Mapped[str | None] = mapped_column(default=None) #change this name
    vendor: Mapped[str] = mapped_column(String)
    
    __mapper_args__ = {
        'polymorphic_identity': 'tunnel',
        'polymorphic_on': vendor
    }
    
    tasks: Mapped[list["Task"]] = relationship(back_populates="tunnel", cascade='all, delete') # type: ignore

