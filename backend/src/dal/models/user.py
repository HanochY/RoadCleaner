from dal.models._base import Common
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4, UUID
from sqlalchemy.dialects.postgresql import UUID as SQL_UUID

class User(Common):
    __tablename__ = 'user'
    
    name: Mapped[str]
    password: Mapped[str]
    admin: Mapped[bool]
