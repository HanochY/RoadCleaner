from collections.abc import Sequence
from uuid import UUID
from utils.exceptions import *
from dal.repository import SQLAlchemyRepository
from dal.db_manager import generate_db_session
from fastapi import HTTPException, status
from api.main.controllers._crud import Controller
from api.main.types.device_user import DeviceUserPublic, DeviceUserFullInput, DeviceUserPartialInput
from api.main.types.user import UserPrivate
from dal.models.device_user import DeviceUser as DeviceUserModel
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload
from sqlalchemy import select

class DeviceUserController(Controller[DeviceUserModel, DeviceUserFullInput, DeviceUserPartialInput, DeviceUserPublic]):
    db_model = DeviceUserModel
    
    def __init__(self) -> None:
        self.repository = SQLAlchemyRepository(Model=self.db_model)
    
    async def create(self, current_user: UserPrivate, data: DeviceUserFullInput) -> UUID:
        try:
            async for session in generate_db_session():
                entity: DeviceUserModel = await self.repository.create(session=session, author_id=current_user.id, **(data.model_dump()))
                await session.commit()
                await session.refresh(entity)
        except TypeError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
        return entity.id 
    
    async def read_by_id(self, id: UUID) -> DeviceUserPublic:
        async for session in generate_db_session():
            result: DeviceUserModel | None = await self.repository.read_one(statement=select(DeviceUserModel).where(DeviceUserModel.id==id).options(joinedload(DeviceUserModel.interfaces)), session=session)  
        if result: return DeviceUserPublic(**(result.__dict__))
        else: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    async def read_all(self) -> list[DeviceUserPublic]:
        async for session in generate_db_session():
            results: Sequence[DeviceUserModel] = await self.repository.read_all(statement=select(DeviceUserModel).options(joinedload(DeviceUserModel.interfaces)), session=session)
        if results: return [DeviceUserPublic(**(entity.__dict__)) for entity in results]
        else: raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    async def update(self, current_user: UserPrivate, id: UUID, new_data: DeviceUserPartialInput) -> None:
        try:
            async for session in generate_db_session():
                await self.repository.update(id=id, session=session, author_id=current_user.id, **(new_data.model_dump()))
                await session.commit()
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
        return None
    
    async def partial_update(self, current_user: UserPrivate, id: UUID, new_data: DeviceUserPartialInput) -> DeviceUserPublic:
        try:
            async for session in generate_db_session():
                print("stst")
                entity = await self.repository.update(id=id, session=session, author_id=current_user.id, **(new_data.model_dump()))
                await session.commit()
                await session.refresh(entity)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
        return DeviceUserPublic(**(entity.__dict__))

    async def delete(self, id: UUID) -> None:
        try:
            async for session in generate_db_session():
                await self.repository.delete(id=id, session=session)
                await session.commit()
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return None
    
    