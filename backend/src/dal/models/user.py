from dal.models._base import Common
from sqlalchemy.orm import Mapped

class User(Common):
    __tablename__ = 'user'
    
    name: Mapped[str]
    password: Mapped[str]
    admin: Mapped[bool]
