from api.main.types._generic import GenericPublic, GenericPrivate, GenericFullInput, GenericPartialInput
from pydantic import BaseModel, field_validator
from ipaddress import IPv4Address
from uuid import UUID


class InterfacePublic(BaseModel, GenericPublic):
    id: UUID
    name: str
    ip: IPv4Address
    device_id: UUID
    tunnel_id: UUID

class InterfacePrivate(BaseModel, GenericPrivate):
    id: UUID
    name: str
    ip: IPv4Address
    device_id: UUID
    tunnel_id: UUID
    
class InterfaceFullInput(BaseModel, GenericFullInput):
    name: str
    ip: IPv4Address
    device_id: UUID
    tunnel_id: UUID

class InterfacePartialInput(BaseModel, GenericPartialInput):
    name: str | None
    ip: IPv4Address | None
    device_id: UUID | None
    tunnel_id: UUID | None