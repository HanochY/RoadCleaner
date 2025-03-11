from collections.abc import Sequence
from uuid import UUID
from utils.exceptions import *
from dal.repository import SQLAlchemyRepository
from dal.db_manager import generate_db_session
from fastapi import HTTPException, status
from api.main.controllers._crud import Controller
from api.main.types.device_type import DeviceTypePublic, DeviceTypeFullInput, DeviceTypePartialInput
from api.main.types.user import UserPrivate
from dal.models.device_type import DeviceType as DeviceTypeModel
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import select

class DeviceTypeController(Controller[DeviceTypeModel, DeviceTypeFullInput, DeviceTypePartialInput, DeviceTypePublic]):
    db_model = DeviceTypeModel
    
    def __init__(self) -> None:
        self.repository = SQLAlchemyRepository(Model=self.db_model)
    
    async def create(self, current_user: UserPrivate, data: DeviceTypeFullInput) -> UUID:
        try:
            print(data.model_dump())
            async for session in generate_db_session():
                entity: DeviceTypeModel = await self.repository.create(session=session, author_id=current_user.id, **(data.model_dump()))
                await session.commit()
                await session.refresh(entity)
        except TypeError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return entity.id 
    
    async def read_by_id(self, id: UUID) -> DeviceTypePublic:
        async for session in generate_db_session():
            result: DeviceTypeModel | None = await self.repository.read_one(statement=select(DeviceTypeModel).where(id==id), session=session)  
        if result: return DeviceTypePublic(**(result.__dict__))
        else: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    async def read_all(self) -> list[DeviceTypePublic]:
        async for session in generate_db_session():
            results: Sequence[DeviceTypeModel] = await self.repository.read_all(statement=select(DeviceTypeModel), session=session)
        if results: return [DeviceTypePublic(**(entity.__dict__)) for entity in results]
        else: raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    async def update(self, current_user: UserPrivate, id: UUID, new_data: DeviceTypeFullInput) -> None:
        try:
            async for session in generate_db_session():
                await self.repository.update(id=id, session=session, author_id=current_user.id, **(new_data.model_dump()))
                await session.commit()
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
        return None
    
    async def partial_update(self, current_user: UserPrivate, id: UUID, new_data: DeviceTypePartialInput) -> DeviceTypePublic:
        try:
            async for session in generate_db_session():
                entity = await self.repository.update(id=id, session=session, author_id=current_user.id, **(new_data.model_dump()))
                await session.commit()
                await session.refresh(entity)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
        return DeviceTypePublic(**(entity.__dict__))
    
    async def delete(self, current_user: UserPrivate, id: UUID) -> None:
        try:
            async for session in generate_db_session():
                await self.repository.delete(id=id, session=session, author_id=current_user.id)
                await session.commit()
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return None
    
    async def undelete(self, id: UUID) -> DeviceTypePublic:
        try:
            async for session in generate_db_session():
                entity = await self.repository.undelete(id=id, session=session)
                await session.commit()
                await session.refresh(entity)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return DeviceTypePublic(**(entity.__dict__))
    
    async def hard_delete(self, current_user: UserPrivate, id: UUID) -> None:
        try:
            async for session in generate_db_session():
                await self.repository.hard_delete(id=id, session=session)
                await session.commit()
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return None
    
    