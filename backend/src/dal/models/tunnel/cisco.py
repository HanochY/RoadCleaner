from dal.models.tunnel._base import Tunnel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from uuid import UUID

class CiscoTunnel(Tunnel):
    __tablename__ = 'tunnel_details_cisco'
    
    id: Mapped[UUID] = mapped_column(ForeignKey("tunnel.id"), primary_key=True)
    keychain_inner: Mapped[str | None] = mapped_column(default=None)
    keychain_outer: Mapped[str | None] = mapped_column(default=None)

    __mapper_args__ = {
        'polymorphic_identity': 'tunnel_cisco'
    }