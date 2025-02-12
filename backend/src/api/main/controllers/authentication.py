from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, SecurityScopes
from jwt import DecodeError

from api.main.security.tokens import TokenData
from dal.models._base import Common as CommonModel
from utils.passwords import verify_password
from api.main.security.tokens import (
    FastAPIBearerToken,
    encode_access_token,
    decode_access_token,
    oauth2_scheme,
)
from types.user import UserPublic
from dal.models.user import User as UserModel
from dal.repository import SQLModelRepository
from sqlalchemy.ext.asyncio import AsyncSession 
from dal.db_manager import get_db_session
from config.provider import ConfigProvider
from uuid import UUID
  
app_settings = ConfigProvider.main_app_settings()
class AuthenticationController:
    
    repository = SQLModelRepository(Model=UserModel)
    
    async def get_user(self, uid: UUID, session: AsyncSession) -> UserPublic:
        user = await self.repository.read(UserModel.id == uid, session=session)
        return user or None
    
    async def find_user_by_username(self, username: str, session: AsyncSession) -> UserPublic | tuple[UserPublic]:
        user: UserModel = (await self.repository.read(session=session, filter=UserModel.name == username))[0]
        return user or None

    async def get_current_user(self, security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)) -> UserPublic:
        if security_scopes.scopes:
            authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        else:
            authenticate_value = "Bearer"
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )
        try:
            token_data: TokenData | None = await decode_access_token(token)
        except DecodeError:
            raise credentials_exception
        async for session in get_db_session():
            user = await self.get_user(token_data.sub, session)
        if user is None:
            raise credentials_exception
        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
        return user

    async def authenticate_for_access_token(self, form_data: OAuth2PasswordRequestForm = Depends()) -> FastAPIBearerToken:
        try:
            async for session in get_db_session():
                user = await self.find_user_by_username(form_data.username, session)
            if user:
                correct_password_hash = user.password
                if verify_password(form_data.password, correct_password_hash):
                    token = encode_access_token(TokenData(sub=user.id,
                                                                    scopes=form_data.scopes,
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