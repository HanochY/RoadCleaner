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
                                            "device_type:read": "Read device types.",
                                            "device_type": "CRUD device types.",
                                            "device:read": "Read devices.",
                                            "device": "CRUD devices.",
                                            "interface:read": "Read interfaces.",
                                            "interface": "CRUD interfaces.",
                                            "site:read": "Read sites.",
                                            "site": "CRUD sites.",
                                            "tunnel:read": "Read sites.",
                                            "tunnel": "CRUD sites.",
                                            "user:read": "Read users.",
                                            "user": "CRUD users.",
                                            "self:read": "Read information about the current user.",
                                            "self": "CRUD current user.",
                                        }
                                    )  
class TokenData(BaseModel):
    sub: UUID
    scopes: list[str] = []
    exp: datetime = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
class OAuthToken(BaseModel):
    access_token: str
    token_type: str

class OAuthBearerToken(OAuthToken):
    access_token: str
    token_type: str = TOKEN_TYPE_BEARER
    
def encode_access_token(data: TokenData) -> str:
    data_dump = data.model_dump()
    data_dump['sub'] = str(data.sub)
    data_dump['scopes'] = ' '.join(data.scopes)
    return(encode(data_dump, SECRET_KEY, ALGORITHM))

def decode_access_token(token: str) -> TokenData | None:
    print("aaassss")
    try:
        data = decode(token, SECRET_KEY, [ALGORITHM])
        print(data)
    except Exception as e:
        print(str(e))
    print(TokenData(sub=UUID(data['sub']), scopes=data['scopes'].split(), exp=data['exp']))
    return TokenData(sub=UUID(data['sub']), scopes=data['scopes'].split(), exp=data['exp'])