from collections.abc import Sequence
from uuid import UUID
from utils.exceptions import *
from dal.repository import SQLAlchemyRepository
from dal.db_manager import generate_db_session
from fastapi import HTTPException, status
from api.main.controllers._crud import Controller
from api.main.types.tunnel.juniper import JuniperTunnelPublic, JuniperTunnelFullInput, JuniperTunnelPartialInput
from api.main.types.user import UserPrivate
from dal.models.tunnel.juniper import JuniperTunnel as JuniperTunnelModel
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload
from sqlalchemy import select

class JuniperTunnelController(Controller[JuniperTunnelModel, JuniperTunnelFullInput, JuniperTunnelPartialInput, JuniperTunnelPublic]):
    db_model = JuniperTunnelModel
    
    def __init__(self) -> None:
        self.repository = SQLAlchemyRepository(Model=self.db_model)
    
    async def create(self, current_user: UserPrivate, data: JuniperTunnelFullInput) -> UUID:
        try:
            async for session in generate_db_session():
                object: JuniperTunnelModel = await self.repository.create(session=session, author_id=current_user.id, **(data.model_dump()))
                await session.commit()
                await session.refresh(object)
        except TypeError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
        return object.id 
    
    async def read_by_id(self, id: UUID) -> JuniperTunnelPublic:
        async for session in generate_db_session():
            result: JuniperTunnelModel | None = await self.repository.read_one(statement=select(JuniperTunnelModel).where(JuniperTunnelModel.id==id).options(joinedload(JuniperTunnelModel.tasks)), session=session)  
        if result: return JuniperTunnelPublic(**(result.__dict__))
        else: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    async def read_all(self) -> list[JuniperTunnelPublic]:
        async for session in generate_db_session():
            results: Sequence[JuniperTunnelModel] = await self.repository.read_all(statement=select(JuniperTunnelModel).options(joinedload(JuniperTunnelModel.tasks)), session=session)
        if results: return [JuniperTunnelPublic(**(object.__dict__)) for object in results]
        else: raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    async def update(self, current_user: UserPrivate, id: UUID, new_data: JuniperTunnelPartialInput) -> None:
        try:
            async for session in generate_db_session():
                await self.repository.update(id=id, session=session, author_id=current_user.id, **(new_data.model_dump()))
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
        return None
    
    async def partial_update(self, current_user: UserPrivate, id: UUID, new_data: JuniperTunnelPartialInput) -> JuniperTunnelPublic:
        try:
            async for session in generate_db_session():
                entity = await self.repository.update(id=id, session=session, author_id=current_user.id, **(new_data.model_dump()))
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
        return JuniperTunnelPublic(**(entity.__dict__))
    
    async def delete(self, current_user: UserPrivate, id: UUID) -> None:
        try:
            async for session in generate_db_session():
                await self.repository.delete(id=id, session=session)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return None
    
    