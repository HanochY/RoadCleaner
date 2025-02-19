from codecs import ignore_errors
from typing_extensions import Annotated
from jwt import InvalidTokenError
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import SecurityScopes

from api.main.security.tokens import (
    oauth2_scheme,
    decode_access_token,
    TokenData
)
from dal.models.user import User as UserModel
from dal.repository import SQLAlchemyRepository
from dal.db_manager import generate_db_session
from pydantic import ValidationError
from utils.scopes import generate_authenticate_value, authorize_scopes
from api.main.types.user import UserPrivate


async def get_current_user(security_scopes: SecurityScopes, 
    token: Annotated[str, Depends(oauth2_scheme)]) -> UserPrivate:
    print('bababa')
    user_repository = SQLAlchemyRepository(Model=UserModel)
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
        print("decpded")
        token_data: TokenData | None = decode_access_token(token)
        print(token_data)
    except (InvalidTokenError, ValidationError):
        raise token_exception
    if not token_data.sub:
        raise token_exception
    if not authorize_scopes(security_scopes, token_data.scopes):
        raise authorization_exception
    async for session in generate_db_session():
        user: UserModel = (await user_repository.read(filter=UserModel.id == token_data.sub, session=session))[0]
    print('qqq')
    return UserPrivate(**user.__dict__)

async def authorize_user(current_user: Annotated[UserPrivate, Security(dependency=get_current_user, scopes=["self:read"])],
) -> UserPrivate:
    if current_user.is_deleted:
        raise HTTPException(status_code=400, detail="Deleted user")
    return current_user