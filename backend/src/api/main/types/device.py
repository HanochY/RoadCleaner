from api.main.types._generic import GenericPublic, GenericPrivate, GenericFullInput, GenericPartialInput
from api.main.types.metadata import Metadata 
from pydantic import BaseModel
from ipaddress import IPv4Address
from uuid import UUID

class DevicePublic(BaseModel, GenericPublic):
    id: UUID
    name: str
    ip: IPv4Address
    type: UUID
    site: UUID
    
class DevicePrivate(Metadata, GenericPrivate):
    id: UUID
    name: str
    ip: IPv4Address
    type: UUID
    site: UUID
    
class DeviceFullInput(BaseModel, GenericFullInput):
    name: str
    ip: IPv4Address
    type: UUID
    site: UUID

class DevicePartialInput(BaseModel, GenericPartialInput):
    name: str | None
    ip: IPv4Address | None
    type: UUID | None
    site: UUID | None