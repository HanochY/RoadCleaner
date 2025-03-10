from api.main.types._generic import GenericPublic, GenericPrivate, GenericFullInput, GenericPartialInput
from api.main.types.metadata import Metadata 
from api.main.types.interface import InterfacePublic, InterfacePrivate 
from pydantic import BaseModel, field_validator
from ipaddress import IPv4Address
from uuid import UUID
from typing import Any

class DevicePublic(BaseModel, GenericPublic):
    id: UUID
    name: str
    ip: IPv4Address
    type_id: UUID
    site_id: UUID
    interfaces: list[InterfacePublic]
    
    @field_validator('interfaces', mode='before')
    def repack_tasks(cls, interfaces: list[Any]) -> list[InterfacePublic]:
        return [InterfacePublic(**(interface.__dict__)) for interface in interfaces]
    
class DevicePrivate(Metadata, GenericPrivate):
    id: UUID
    name: str
    ip: IPv4Address
    type_id: UUID
    site_id: UUID
    interfaces: list[InterfacePrivate]
    
    @field_validator('interfaces', mode='before')
    def repack_tasks(cls, interfaces: list[Any]) -> list[InterfacePrivate]:
        return [InterfacePrivate(**(interface.__dict__)) for interface in interfaces]
    
class DeviceFullInput(BaseModel, GenericFullInput):
    name: str
    ip: str
    type_id: UUID
    site_id: UUID
    
    @field_validator('ip')
    def validate_ip(cls, value):
        return str(IPv4Address(value))
    class Config(GenericFullInput.Config):
        pass

class DevicePartialInput(BaseModel, GenericPartialInput):
    name: str | None = None
    ip: str | None = None
    type_id: UUID | None = None
    site_id: UUID | None = None
    
    @field_validator('ip')
    def validate_ip(cls, value):
        if value: return str(IPv4Address(value))
        else: return None
    class Config(GenericPartialInput.Config):
        pass