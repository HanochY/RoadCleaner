from api.main.types._generic import GenericPublic, GenericPrivate, GenericFullInput, GenericPartialInput
from pydantic import BaseModel, AfterValidator, Field
from uuid import UUID
from typing_extensions import Annotated 
from utils.validate_list_unique import validate_list_unique

class TunnelPublic(BaseModel, GenericPublic):
    id: UUID
    name: str
    interfaces: Annotated[list[UUID], AfterValidator(validate_list_unique)] = Field(max_length=2, min_length=2)
    
class TunnelPrivate(BaseModel, GenericPrivate):
    id: UUID
    name: str
    interfaces: Annotated[list[UUID], AfterValidator(validate_list_unique)] = Field(max_length=2, min_length=2)
    
class TunnelFullInput(BaseModel, GenericFullInput):
    name: str
    interfaces: Annotated[list[UUID], AfterValidator(validate_list_unique)] = Field(max_length=2, min_length=2)

class TunnelPartialInput(BaseModel, GenericPartialInput):
    name: str | None
    interfaces: Annotated[list[UUID], AfterValidator(validate_list_unique)] = Field(max_length=2) | None