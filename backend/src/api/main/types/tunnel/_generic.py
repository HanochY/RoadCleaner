from api.main.types._generic import GenericPublic, GenericPrivate, GenericFullInput, GenericPartialInput
from api.main.types.metadata import Metadata 
from api.main.types.task import TaskPublic, TaskPrivate 
from pydantic import BaseModel, field_validator
from uuid import UUID
from datetime import datetime
from typing import Any
class TunnelPublic(BaseModel, GenericPublic):
    id: UUID
    name: str
    interface_inner_id: UUID | None
    interface_outer_id: UUID | None
    hardened_at: datetime | None = None
    hardened_by: str | None = None
    tasks: list[TaskPublic]
    
    @field_validator('tasks', mode='before')
    def repack_tasks(cls, tasks: list[Any]) -> list[TaskPublic]:
        return [TaskPublic(**(task.__dict__)) for task in tasks]
    
class TunnelPrivate(Metadata, GenericPrivate):
    id: UUID
    name: str
    interface_inner_id: UUID | None
    interface_outer_id: UUID | None
    hardened_at: datetime | None = None
    hardened_by: str | None = None
    tasks: list[TaskPrivate]
        
    @field_validator('tasks', mode='before')
    def repack_tasks(cls, tasks: list[Any]) -> list[TaskPrivate]:
        return [TaskPrivate(**(task.__dict__)) for task in tasks]
    
class TunnelFullInput(BaseModel, GenericFullInput):
    name: str
    interface_inner_id: UUID | None
    interface_outer_id: UUID | None
    class Config(GenericFullInput.Config):
        pass

class TunnelPartialInput(BaseModel, GenericPartialInput):
    name: str | None = None
    interface_inner_id: UUID | None = None
    interface_outer_id: UUID | None = None
    class Config(GenericPartialInput.Config):
        pass
