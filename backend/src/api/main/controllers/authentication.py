from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from config.apps._schema import AppSettings
from utils.passwords import verify_password
from api.main.security.tokens import (
    OAuthBearerToken,
    encode_access_token,
    TokenData
)
from dal.models.user import User as UserModel
from dal.repository import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession 
from dal.db_manager import generate_db_session
  
class AuthenticationController:
    
    repository = SQLAlchemyRepository(Model=UserModel)
    
    async def find_user_by_username(self, username: str, session: AsyncSession) -> UserModel:
        user: UserModel = (await self.repository.read(session=session, filter=UserModel.name == username))[0]
        return user or None

    async def authenticate_for_access_token(self, form_data: OAuth2PasswordRequestForm = Depends()) -> OAuthBearerToken:
        try:
            async for session in generate_db_session():
                user = await self.find_user_by_username(form_data.username, session)
            requested_scopes = form_data.scopes
            if user:
                allowed_scopes = ["device_type:read",
                                            "device:read",
                                            "device",
                                            "interface:read",
                                            "interface",
                                            "site:read",
                                            "site",
                                            "tunnel:read",
                                            "tunnel",
                                            "self:read",
                                            "self"]
                if user.admin:
                    allowed_scopes = allowed_scopes + [
                                            "device_type",
                                            "user:read",
                                            "user",]
                correct_password_hash = user.password
                if verify_password(form_data.password, correct_password_hash):
                    token = encode_access_token(TokenData(sub=user.id,
                                                                    scopes=[scope for scope in requested_scopes if scope in allowed_scopes]))
                    return OAuthBearerToken(access_token=token)
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
            raise