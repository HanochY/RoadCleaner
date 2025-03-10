from api.main.types._generic import GenericPublic, GenericPrivate, GenericFullInput, GenericPartialInput
from api.main.types.metadata import Metadata 
from api.main.types.device import DevicePublic, DevicePrivate 
from pydantic import BaseModel, field_validator
from uuid import UUID
from typing import Any
class SitePublic(BaseModel, GenericPublic):
    id: UUID
    name: str
    devices: list[DevicePublic]
    
    @field_validator('devices', mode='before')
    def repack_tasks(cls, devices: list[Any]) -> list[DevicePublic]:
        return [DevicePublic(**(device.__dict__)) for device in devices]
    
class SitePrivate(Metadata, GenericPrivate):
    id: UUID
    name: str
    devices: list[DevicePrivate]
    
    @field_validator('devices', mode='before')
    def repack_tasks(cls, devices: list[Any]) -> list[DevicePrivate]:
        return [DevicePrivate(**(device.__dict__)) for device in devices]
    
class SiteFullInput(BaseModel, GenericFullInput):
    name: str
    class Config(GenericFullInput.Config):
        pass
class SitePartialInput(BaseModel, GenericPartialInput):
    name: str | None = None
    class Config(GenericPartialInput.Config):
        pass