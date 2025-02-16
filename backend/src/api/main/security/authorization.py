from typing_extensions import Annotated
from jwt import InvalidTokenError
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import SecurityScopes

from api.main.security.tokens import (
    oauth2_scheme,
    decode_access_token,
    TokenData
)
from dal import repository
from dal.models.user import User as UserModel
from dal.repository import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession 
from dal.db_manager import get_db_session
from config.provider import ConfigProvider
from uuid import UUID
from pydantic import ValidationError
from utils.scopes import generate_authenticate_value, authorize_scopes

class AuthorizationManager():
    user_repository = SQLAlchemyRepository(Model=UserModel)
    
    async def get_current_user(
        self,
        security_scopes: SecurityScopes, 
        token: Annotated[str, Depends(oauth2_scheme)]):
        print('b')
        authenticate_value = await generate_authenticate_value(security_scopes)
        token_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )
        authorization_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )
        try:
            token_data: TokenData | None = await decode_access_token(token)
        except (InvalidTokenError, ValidationError):
            raise token_exception
        if not token_data.sub:
            raise token_exception
        if not authorize_scopes(security_scopes, token_data.scopes):
            raise authorization_exception
        user: UserModel = await self.user_repository.read(get_db_session(), UserModel.id == token_data.sub)
        return user
    
    async def authorize_user(
        current_user: Annotated[UserModel, Security(get_current_user, scopes=["self:read"])],
    ):
        
        if current_user.is_deleted:
            raise HTTPException(status_code=400, detail="Deleted user")
        return current_user
    
    