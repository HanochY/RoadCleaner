from uuid import UUID
from dal.repository import SQLAlchemyRepository
from dal.db_manager import generate_db_session
from api.main.types.user import UserFullInput
from dal.models.user import User as UserModel
from utils.passwords import hash_password
import asyncio

data = {
    "name": "admin",
    "password": "hJgmmZMdoMhvMylbsTQiRYXW44g61HDjain7PVtPHEZxJoMD3PSy4LxWQtwky2cv",
    "admin" : True
}
new_user = UserFullInput(**data)

async def init_admin():
    async for session in generate_db_session():
        new_user.password = hash_password(new_user.password)
        object = await SQLAlchemyRepository(UserModel).create(session=session, author_id=UUID(int=0), **(new_user.model_dump()))
        await session.commit()
        await session.refresh(object)
asyncio.run(main=init_admin())