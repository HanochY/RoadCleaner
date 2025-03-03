from collections.abc import Sequence
from uuid import UUID
from utils.exceptions import *
from dal.repository import SQLAlchemyRepository
from dal.db_manager import generate_db_session
from fastapi import HTTPException, status
from api.main.controllers._crud import Controller
from api.main.types.tunnel.cisco import CiscoTunnelPublic, CiscoTunnelFullInput, CiscoTunnelPartialInput
from api.main.types.user import UserPrivate
from dal.models.tunnel.cisco import CiscoTunnel as CiscoTunnelModel
from sqlalchemy.orm.exc import NoResultFound

class CiscoTunnelController(Controller[CiscoTunnelModel, CiscoTunnelFullInput, CiscoTunnelPartialInput, CiscoTunnelPublic]):
    db_model = CiscoTunnelModel
    
    def __init__(self) -> None:
        self.repository = SQLAlchemyRepository(Model=self.db_model)
    
    async def create(self, current_user: UserPrivate, data: CiscoTunnelFullInput) -> UUID:
        try:
            async for session in generate_db_session():
                object: CiscoTunnelModel = await self.repository.create(session=session, author_id=current_user.id, **(data.model_dump()))
                await session.commit()
                await session.refresh(object)
        except TypeError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
        return object.id 
    
    async def read_by_id(self, id: UUID) -> CiscoTunnelPublic:
        async for session in generate_db_session():
            results: Sequence[CiscoTunnelModel] | None = await self.repository.read(filter=id==id, session=session)  
        if results: return CiscoTunnelPublic(**(results[0].__dict__))
        else: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    async def read_all(self) -> list[CiscoTunnelPublic]:
        async for session in generate_db_session():
            results: Sequence[CiscoTunnelModel] | None = await self.repository.read(session=session)
        if results: return [CiscoTunnelPublic(**(object.__dict__)) for object in results]
        else: raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    async def update(self, current_user: UserPrivate, id: UUID, new_data: CiscoTunnelPartialInput) -> None:
        try:
            async for session in generate_db_session():
                await self.repository.update(id=id, session=session, author_id=current_user.id, **(new_data.model_dump()))
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
        return None
    
    async def partial_update(self, current_user: UserPrivate, id: UUID, new_data: CiscoTunnelPartialInput) -> CiscoTunnelPublic:
        try:
            async for session in generate_db_session():
                entity = await self.repository.update(id=id, session=session, author_id=current_user.id, **(new_data.model_dump()))
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
        return CiscoTunnelPublic(**(entity.__dict__))
    
    async def delete(self, current_user: UserPrivate, id: UUID) -> None:
        try:
            async for session in generate_db_session():
                await self.repository.delete(id=id, session=session, author_id=current_user.id)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return None
    
    async def undelete(self, current_user: UserPrivate, id: UUID) -> CiscoTunnelPublic:
        try:
            async for session in generate_db_session():
                entity = await self.repository.undelete(id=id, session=session, author_id=current_user.id)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return CiscoTunnelPublic(**(entity.__dict__))
    
    async def hard_delete(self, current_user: UserPrivate, id: UUID) -> None:
        try:
            async for session in generate_db_session():
                await self.repository.hard_delete(id=id, session=session, author_id=current_user.id)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return None
    
    