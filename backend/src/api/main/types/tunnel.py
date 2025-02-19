from api.main.types._generic import GenericPublic, GenericPrivate, GenericFullInput, GenericPartialInput
from api.main.types.metadata import Metadata 
from pydantic import BaseModel, AfterValidator, Field
from uuid import UUID
from typing_extensions import Annotated 
from utils.validate_list_unique import validate_list_unique
from datetime import datetime

class TunnelPublic(BaseModel, GenericPublic):
    unique_name: str = Field(max_length=64)
    name: str
    interfaces: Annotated[list[UUID], AfterValidator(validate_list_unique)] = Field(max_length=2, min_length=2)
    reinforced_at: datetime | None
    reinforced_by: str | None
    
class TunnelPrivate(Metadata, GenericPrivate):
    unique_name: str = Field(max_length=64)
    name: str
    interfaces: Annotated[list[UUID], AfterValidator(validate_list_unique)] = Field(max_length=2, min_length=2)
    reinforced_at: datetime | None
    reinforced_by: str | None
    
class TunnelFullInput(BaseModel, GenericFullInput):
    unique_name: str = Field(max_length=64)
    name: str
    interfaces: Annotated[list[UUID], AfterValidator(validate_list_unique)] = Field(max_length=2, min_length=2)
    reinforced_at: datetime | None
    reinforced_by: str | None

class TunnelPartialInput(BaseModel, GenericPartialInput):
    unique_name: str | None = Field(max_length=64) 
    name: str | None
    interfaces: Annotated[list[UUID], AfterValidator(validate_list_unique)] | None = Field(max_length=2, min_length=2) 
    reinforced_at: datetime | None
    reinforced_by: str | None