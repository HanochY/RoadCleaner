from collections.abc import Sequence
from uuid import UUID, uuid4
from jwt import DecodeError 
from dal.repository import SQLAlchemyRepository
from dal.db_manager import get_db_session
from fastapi import HTTPException, status, Depends
from api.main.controllers._crud import Controller
from api.main.types.user import UserPublic, UserFullInput, UserPartialInput
from dal.models.user import User as UserModel
from sqlalchemy.orm.exc import NoResultFound


from utils.passwords import hash_password
class UserController(Controller[UserModel, UserFullInput, UserPartialInput, UserPublic]):
    db_model = UserModel
    
    def __init__(self) -> None:
        self.repository = SQLAlchemyRepository(Model=self.db_model)
    
    async def create(self, data: UserFullInput) -> UUID:
        try:
            async for session in get_db_session():
                print('ww')
                data.password = hash_password(data.password)
                object: UserModel = await self.repository.create(session=session, author_id=uuid4(), **(data.model_dump()))
                await session.commit()
                await session.refresh(object)
                print('aa')
        except TypeError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return object.id 
    
    async def read_by_id(self, id: UUID) -> UserPublic:
        async for session in get_db_session():
            results: Sequence[UserModel] | None = await self.repository.read(filter=id==id, session=session)  
        if results: return UserPublic(results[0])
        else: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    async def read_all(self) -> list[UserPublic]:
        async for session in get_db_session():
            results: Sequence[UserModel] | None = await self.repository.read(session=session)
        if results: return [UserPublic(object) for object in results]
        else: raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    async def update(self, id: UUID, new_data: UserPartialInput) -> None:
        try:
            async for session in get_db_session():
                await self.repository.update(id=id, session=session, **new_data)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except TypeError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return None
    
    async def partial_update(self, id: UUID, new_data: UserPartialInput) -> UserPublic:
        try:
            async for session in get_db_session():
                entity = await self.repository.update(id=id, session=session, **new_data)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except TypeError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return UserPublic(entity)
    
    async def delete(self, id: UUID) -> None:
        try:
            async for session in get_db_session():
                await self.repository.delete(id=id, session=session)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return None
    
    async def undelete(self, id: UUID) -> UserPublic:
        try:
            async for session in get_db_session():
                entity = await self.repository.undelete(id=id, session=session)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return UserPublic(entity)
    
    async def hard_delete(self, id: UUID) -> None:
        try:
            async for session in get_db_session():
                await self.repository.hard_delete(id=id, session=session)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return None
    
    