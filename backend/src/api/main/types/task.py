from api.main.types._generic import GenericPublic, GenericPrivate, GenericFullInput, GenericPartialInput
from api.main.types.metadata import Metadata 
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class TaskPublic(BaseModel, GenericPublic):
    id: UUID
    name: str
    subject: UUID
    details: str
    start_time: datetime
    end_time: datetime | None = None
    
class TaskPrivate(Metadata, GenericPrivate):
    id: UUID
    name: str
    subject: UUID
    details: str
    start_time: datetime
    end_time: datetime | None = None
    
class TaskFullInput(BaseModel, GenericFullInput):
    id: UUID
    name: str
    subject: UUID
    details: str


class TaskPartialInput(BaseModel, GenericPartialInput):
    id: UUID | None = None
    name: str | None = None
    subject: UUID | None = None
    details: str | None = None