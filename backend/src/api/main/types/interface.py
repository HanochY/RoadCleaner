from api.main.types._generic import GenericPublic, GenericPrivate, GenericFullInput, GenericPartialInput
from api.main.types.metadata import Metadata 
from pydantic import BaseModel, field_validator
from ipaddress import IPv4Address
from uuid import UUID


class InterfacePublic(BaseModel, GenericPublic):
    id: UUID
    name: str
    ip: IPv4Address
    device_id: UUID
    tunnel_id: UUID | None = None
    
class InterfacePrivate(Metadata, GenericPrivate):
    id: UUID
    name: str
    ip: IPv4Address
    device_id: UUID
    tunnel_id: UUID | None = None
    
class InterfaceFullInput(BaseModel, GenericFullInput):
    name: str
    ip: str
    device_id: UUID
    tunnel_id: UUID | None = None
    
    @field_validator('ip')
    def validate_ip(cls, value):
        return str(IPv4Address(value))

class InterfacePartialInput(BaseModel, GenericPartialInput):
    name: str | None = None
    ip: str | None = None
    device_id: UUID | None = None
    tunnel_id: UUID | None = None
    
    @field_validator('ip')
    def validate_ip(cls, value):
        if value: return str(IPv4Address(value))
        else: return None