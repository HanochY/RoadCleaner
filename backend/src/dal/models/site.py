from dal.models._base import Common
from sqlalchemy.orm import Mapped, relationship, mapped_column
from uuid import uuid4, UUID
from sqlalchemy.dialects.postgresql import UUID as SQL_UUID

class Site(Common):
    __tablename__ = 'site'
    
    id: Mapped[UUID] = mapped_column(SQL_UUID(as_uuid=True), default=uuid4, primary_key=True)
    name: Mapped[str]
    devices: Mapped[list["Device"]] = relationship(back_populates="site") # type: ignore