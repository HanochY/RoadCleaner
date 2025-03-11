
from uuid import UUID
from dal.models._base import Common
from api.main.types._generic import GenericOutput, GenericFullInput, GenericPartialInput
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T', bound=Common) # Any conventional SQLAlchemy ORM object
C = TypeVar('C', bound=GenericFullInput)  # Any Create object
U = TypeVar('U', bound=GenericPartialInput)  # Any Update object
O = TypeVar('O', bound=GenericOutput)  # Any Output object
class Controller(ABC, Generic[T, C, U, O]):
    db_model: type[T]
    
    @abstractmethod
    async def create(self, data: C) -> UUID:        
        pass
    @abstractmethod
    async def read_by_id(self, id: UUID) -> O:
        pass
    @abstractmethod
    async def read_all(self) -> list[O]:
        pass
    @abstractmethod
    async def update(self, id: UUID, new_data: U) -> None:
        pass
    @abstractmethod
    async def partial_update(self, id: UUID, new_data: U) -> O:
        pass
    @abstractmethod
    async def delete(self, id: UUID) -> None:
        pass