from collections.abc import Sequence
from uuid import UUID
from utils.exceptions import *
from dal.repository import SQLAlchemyRepository
from dal.db_manager import generate_db_session
from fastapi import HTTPException, status
from api.main.controllers._crud import Controller
from api.main.types.site import SitePublic, SiteFullInput, SitePartialInput
from api.main.types.user import UserPrivate
from dal.models.site import Site as SiteModel
from dal.models.device import Device as DeviceModel
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload
from sqlalchemy import select

class SiteController(Controller[SiteModel, SiteFullInput, SitePartialInput, SitePublic]):
    db_model = SiteModel
    
    def __init__(self) -> None:
        self.repository = SQLAlchemyRepository(Model=self.db_model)
    
    async def create(self, current_user: UserPrivate, data: SiteFullInput) -> UUID:
        try:
            async for session in generate_db_session():
                entity: SiteModel = await self.repository.create(session=session, author_id=current_user.id, **(data.model_dump()))
                await session.commit()
                await session.refresh(entity)
        except TypeError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
        return entity.id 
    
    async def read_by_id(self, id: UUID) -> SitePublic:
        async for session in generate_db_session():
            result: SiteModel | None = await self.repository.read_one(statement=select(SiteModel).where(SiteModel.id==id).options(joinedload(SiteModel.devices).joinedload(DeviceModel.interfaces)), session=session) 
        print(str(result)) 
        if result: return SitePublic(**(result.__dict__))
        else: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    async def read_all(self) -> list[SitePublic]:
        async for session in generate_db_session():
            results: Sequence[SiteModel] = await self.repository.read_all(statement=select(SiteModel).options(joinedload(SiteModel.devices).joinedload(DeviceModel.interfaces)), session=session)
        if results: return [SitePublic(**(entity.__dict__)) for entity in results]
        else: raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    async def update(self, current_user: UserPrivate, id: UUID, new_data: SitePartialInput) -> None:
        try:
            async for session in generate_db_session():
                await self.repository.update(id=id, session=session, author_id=current_user.id, **(new_data.model_dump()))
                await session.commit()
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
        return None
    
    async def partial_update(self, current_user: UserPrivate, id: UUID, new_data: SitePartialInput) -> SitePublic:
        try:
            async for session in generate_db_session():
                entity = await self.repository.update(id=id, session=session, author_id=current_user.id, **(new_data.model_dump()))
                await session.commit()
                await session.refresh(entity)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))            
        return SitePublic(**(entity.__dict__))

    async def delete(self, current_user: UserPrivate, id: UUID) -> None:
        try:
            async for session in generate_db_session():
                await self.repository.delete(id=id, session=session)
                await session.commit()
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return None
    
    