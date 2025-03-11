from collections.abc import Sequence
from uuid import UUID, uuid4
from jwt import DecodeError 
from dal.repository import SQLAlchemyRepository
from dal.db_manager import generate_db_session
from fastapi import HTTPException, status, Depends
from api.main.controllers._crud import Controller
from api.main.types.user import UserPublic, UserPrivate, UserFullInput, UserPartialInput
from dal.models.user import User as UserModel
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import select
from utils.passwords import hash_password

class UserController(Controller[UserModel, UserFullInput, UserPartialInput, UserPublic]):
    db_model = UserModel
    
    def __init__(self) -> None:
        self.repository = SQLAlchemyRepository(Model=self.db_model)
    
    async def create(self, current_user: UserPrivate, data: UserFullInput) -> UUID:
        try:
            async for session in generate_db_session():
                data.password = hash_password(data.password)
                entity: UserModel = await self.repository.create(session=session, author_id=current_user.id, **(data.model_dump()))
                await session.commit()
                await session.refresh(entity)
        except TypeError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return entity.id 
    
    async def read_by_id(self, id: UUID) -> UserPublic:
        async for session in generate_db_session():
            result: UserModel | None = await self.repository.read_one(statement=select(UserModel).where(UserModel.id==id), session=session)  
        if result: return UserPublic(**(result.__dict__))
        else: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    async def read_all(self) -> list[UserPublic]:
        async for session in generate_db_session():
            results: Sequence[UserModel] = await self.repository.read_all(statement=select(UserModel), session=session)
        if results: return [UserPublic(**(entity.__dict__)) for entity in results]
        else: raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    async def update(self, current_user: UserPrivate, id: UUID, new_data: UserPartialInput) -> None:
        try:
            async for session in generate_db_session():
                await self.repository.update(id=id, session=session, author_id=current_user.id, **(new_data.model_dump()))
                await session.commit()
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
        return None
    
    async def partial_update(self, current_user: UserPrivate, id: UUID, new_data: UserPartialInput) -> UserPublic:
        try:
            async for session in generate_db_session():
                entity = await self.repository.update(id=id, session=session, author_id=current_user.id, **(new_data.model_dump()))
                await session.commit()
                await session.refresh(entity)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except TypeError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
        return UserPublic(**(entity.__dict__))
    
    async def delete(self, current_user: UserPrivate, id: UUID) -> None:
        try:
            async for session in generate_db_session():
                await self.repository.delete(id=id, session=session, author_id=current_user.id)
                await session.commit()
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return None
    
    async def undelete(self, id: UUID) -> UserPublic:
        try:
            async for session in generate_db_session():
                entity = await self.repository.undelete(id=id, session=session)
                await session.commit()
                await session.refresh(entity)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return UserPublic(**(entity.__dict__))
    
    async def hard_delete(self, current_user: UserPrivate, id: UUID) -> None:
        try:
            async for session in generate_db_session():
                await self.repository.hard_delete(id=id, session=session)
                await session.commit()
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return None
    
    