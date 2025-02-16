from collections.abc import Sequence
from uuid import UUID
from utils.exceptions import *
from dal.repository import SQLAlchemyRepository
from dal.db_manager import get_db_session
from fastapi import HTTPException, status
from api.main.controllers._crud import Controller
from types.device_type import DeviceTypePublic, DeviceTypeFullInput, DeviceTypePartialInput
from dal.models.device_type import DeviceType as DeviceTypeModel
from sqlalchemy.orm.exc import NoResultFound

class DeviceTypeController(Controller[DeviceTypeModel, DeviceTypeFullInput, DeviceTypePartialInput, DeviceTypePublic]):
    db_model = type[DeviceTypeModel]
    
    def __init__(self) -> None:
        self.repository = SQLAlchemyRepository(Model=self.db_model)
    
    async def create(self, data: DeviceTypeFullInput) -> UUID:
        try:
            async for session in get_db_session():
                object: DeviceTypeModel = await self.repository.create(session=session, author_id=0, uid=0, **data)
                await session.commit()
                await session.refresh(object)
        except TypeError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return object.id 
    
    async def read_by_id(self, id: UUID) -> DeviceTypePublic:
        async for session in get_db_session():
            results: Sequence[DeviceTypeModel] | None = await self.repository.read(filter=id==id, session=session)  
        if results: return DeviceTypePublic(results[0])
        else: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    async def read_all(self) -> list[DeviceTypePublic]:
        async for session in get_db_session():
            results: Sequence[DeviceTypeModel] | None = await self.repository.read(session=session)
        if results: return [DeviceTypePublic(object) for object in results]
        else: raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    async def update(self, id: UUID, new_data: DeviceTypePartialInput) -> None:
        try:
            async for session in get_db_session():
                await self.repository.update(id=id, session=session, **new_data)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except TypeError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return None
    
    async def partial_update(self, id: UUID, new_data: DeviceTypePartialInput) -> DeviceTypePublic:
        try:
            async for session in get_db_session():
                entity = await self.repository.update(id=id, session=session, **new_data)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except TypeError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return DeviceTypePublic(entity)
    
    async def delete(self, id: UUID) -> None:
        try:
            async for session in get_db_session():
                await self.repository.delete(id=id, session=session)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return None
    
    async def undelete(self, id: UUID) -> DeviceTypePublic:
        try:
            async for session in get_db_session():
                entity = await self.repository.undelete(id=id, session=session)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return DeviceTypePublic(entity)
    
    async def hard_delete(self, id: UUID) -> None:
        try:
            async for session in get_db_session():
                await self.repository.hard_delete(id=id, session=session)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return None
    
    