from collections.abc import Sequence
from uuid import UUID
from utils.exceptions import *
from dal.repository import SQLAlchemyRepository
from dal.db_manager import get_db_session
from fastapi import HTTPException, status
from api.main.controllers._crud import Controller
from types.device import DevicePublic, DeviceFullInput, DevicePartialInput
from dal.models.device import Device as DeviceModel
from sqlalchemy.orm.exc import NoResultFound

class DeviceController(Controller[DeviceModel, DeviceFullInput, DevicePartialInput, DevicePublic]):
    db_model = type[DeviceModel]
    
    def __init__(self) -> None:
        self.repository = SQLAlchemyRepository(Model=self.db_model)
    
    async def create(self, data: DeviceFullInput) -> UUID:
        try:
            async for session in get_db_session():
                object: DeviceModel = await self.repository.create(session=session, author_id=0, uid=0, **data)
                await session.commit()
                await session.refresh(object)
        except TypeError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return object.id 
    
    async def read_by_id(self, id: UUID) -> DevicePublic:
        async for session in get_db_session():
            results: Sequence[DeviceModel] | None = await self.repository.read(filter=id==id, session=session)  
        if results: return DevicePublic(results[0])
        else: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    async def read_all(self) -> list[DevicePublic]:
        async for session in get_db_session():
            results: Sequence[DeviceModel] | None = await self.repository.read(session=session)
        if results: return [DevicePublic(object) for object in results]
        else: raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    async def update(self, id: UUID, new_data: DevicePartialInput) -> None:
        try:
            async for session in get_db_session():
                await self.repository.update(id=id, session=session, **new_data)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except TypeError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return None
    
    async def partial_update(self, id: UUID, new_data: DevicePartialInput) -> DevicePublic:
        try:
            async for session in get_db_session():
                entity = await self.repository.update(id=id, session=session, **new_data)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except TypeError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return DevicePublic(entity)
    
    async def delete(self, id: UUID) -> None:
        try:
            async for session in get_db_session():
                await self.repository.delete(id=id, session=session)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return None
    
    async def undelete(self, id: UUID) -> DevicePublic:
        try:
            async for session in get_db_session():
                entity = await self.repository.undelete(id=id, session=session)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return DevicePublic(entity)
    
    async def hard_delete(self, id: UUID) -> None:
        try:
            async for session in get_db_session():
                await self.repository.hard_delete(id=id, session=session)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return None
    
    