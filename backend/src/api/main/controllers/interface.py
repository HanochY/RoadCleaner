from collections.abc import Sequence
from uuid import UUID
from utils.exceptions import *
from dal.repository import SQLAlchemyRepository
from dal.db_manager import generate_db_session
from fastapi import HTTPException, status
from api.main.controllers._crud import Controller
from api.main.types.interface import InterfacePublic, InterfaceFullInput, InterfacePartialInput
from api.main.types.user import UserPrivate
from dal.models.interface import Interface as InterfaceModel
from sqlalchemy.orm.exc import NoResultFound

class InterfaceController(Controller[InterfaceModel, InterfaceFullInput, InterfacePartialInput, InterfacePublic]):
    db_model = type[InterfaceModel]
    
    def __init__(self) -> None:
        self.repository = SQLAlchemyRepository(Model=self.db_model)
    
    async def create(self, current_user: UserPrivate, data: InterfaceFullInput) -> UUID:
        try:
            async for session in generate_db_session():
                object: InterfaceModel = await self.repository.create(session=session, author_id=current_user.id, **(data.model_dump()))
                await session.commit()
                await session.refresh(object)
        except TypeError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return object.id 
    
    async def read_by_id(self, current_user: UserPrivate, id: UUID) -> InterfacePublic:
        async for session in generate_db_session():
            results: Sequence[InterfaceModel] | None = await self.repository.read(filter=id==id, session=session)  
        if results: return InterfacePublic(results[0])
        else: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    async def read_all(self) -> list[InterfacePublic]:
        async for session in generate_db_session():
            results: Sequence[InterfaceModel] | None = await self.repository.read(session=session)
        if results: return [InterfacePublic(object) for object in results]
        else: raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    async def update(self, current_user: UserPrivate, id: UUID, new_data: InterfacePartialInput) -> None:
        try:
            async for session in generate_db_session():
                await self.repository.update(id=id, session=session, **(new_data.model_dump()))
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except TypeError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return None
    
    async def partial_update(self, current_user: UserPrivate, id: UUID, new_data: InterfacePartialInput) -> InterfacePublic:
        try:
            async for session in generate_db_session():
                entity = await self.repository.update(id=id, session=session, **(new_data.model_dump()))
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except TypeError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return InterfacePublic(entity)
    
    async def delete(self, current_user: UserPrivate, id: UUID) -> None:
        try:
            async for session in generate_db_session():
                await self.repository.delete(id=id, session=session)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return None
    
    async def undelete(self, current_user: UserPrivate, id: UUID) -> InterfacePublic:
        try:
            async for session in generate_db_session():
                entity = await self.repository.undelete(id=id, session=session)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return InterfacePublic(entity)
    
    async def hard_delete(self, current_user: UserPrivate, id: UUID) -> None:
        try:
            async for session in generate_db_session():
                await self.repository.hard_delete(id=id, session=session)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return None
    
    