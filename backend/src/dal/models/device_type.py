from sqlalchemy.orm import Mapped, relationship, mapped_column
from dal.models._base import Base
class DeviceType(Base):
    __tablename__ = 'device_type'

    name: Mapped[str] = mapped_column(primary_key=True)