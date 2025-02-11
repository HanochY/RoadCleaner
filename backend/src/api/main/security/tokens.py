from jwt import DecodeError, InvalidTokenError, encode, decode
from pydantic import BaseModel
from config.provider import ConfigProvider
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID
from datetime import datetime, timezone, timedelta

app_settings = ConfigProvider.main_app_settings(production=False)
SECRET_KEY = app_settings.SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = app_settings.ACCESS_TOKEN_EXPIRE_MINUTES
ALGORITHM = app_settings.ACCESS_TOKEN_ALGORITHM
TOKEN_TYPE_BEARER = "bearer"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token",
                                    scopes={
                                        "self:read": "Read information about the current user.",
                                        "items:read": "Read items.",
                                        "items": "CRUD items.",
                                        "users:read": "Read users.",
                                        "users": "CRUD users.",
                                        }
                                    )  
class TokenData(BaseModel):
    sub: UUID
    scopes: list[str] = []
    exp: datetime = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
class FastAPIToken(BaseModel):
    data: str
    token_type: str
    
    def __init__(self, value):
        self.data = value

class FastAPIBearerToken(FastAPIToken):
    token_type: str = TOKEN_TYPE_BEARER
    
def encode_access_token(data: TokenData) -> str:
    return(encode(data.model_dump(), SECRET_KEY, ALGORITHM))


async def decode_access_token(token: str) -> TokenData | None:
    try:
        data: TokenData = await decode(token, SECRET_KEY, ALGORITHM)
        return TokenData(data)
    except TypeError:
        raise DecodeError