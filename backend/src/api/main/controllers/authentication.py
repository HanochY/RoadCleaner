from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from utils.passwords import verify_password
from api.main.security.tokens import (
    FastAPIBearerToken,
    encode_access_token,
    TokenData
)
from api.main.types.user import UserPublic
from dal.models.user import User as UserModel
from dal.repository import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession 
from dal.db_manager import get_db_session
from config.provider import ConfigProvider
from uuid import UUID
  
app_settings = ConfigProvider.main_app_settings()
class AuthenticationController:
    
    repository = SQLAlchemyRepository(Model=UserModel)
    
    async def find_user_by_username(self, username: str, session: AsyncSession) -> UserModel | tuple[UserModel]:
        user: UserModel = (await self.repository.read(session=session, filter=UserModel.name == username))[0]
        return user or None

    async def authenticate_for_access_token(self, form_data: OAuth2PasswordRequestForm = Depends()) -> FastAPIBearerToken:
        try:
            async for session in get_db_session():
                user = await self.find_user_by_username(form_data.username, session)
            if user:
                scopes = ["device_type:read",
                                            "device:read",
                                            "device",
                                            "interface:read",
                                            "interface",
                                            "site:read",
                                            "site",
                                            "tunnel:read",
                                            "tunnel",]
                if user.admin:
                    scopes = scopes + [
                                            "device_type",
                                            "user:read",
                                            "user",]
                correct_password_hash = user.password
                if verify_password(form_data.password, correct_password_hash):
                    token = encode_access_token(TokenData(sub=user.id,
                                                                    scopes=scopes,
                                                                    exp=timedelta(minutes=app_settings.ACCESS_TOKEN_EXPIRE_MINUTES)))
                    return FastAPIBearerToken(token)
                else:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Incorrect username or password",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
            else:
                raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found",
                        headers={"WWW-Authenticate": "Bearer"},
                    )

        except Exception as e:
            print(e)