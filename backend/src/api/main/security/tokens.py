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
                                            "device_type": "Create, Update and Delete device types.",
                                            "device:read": "Read devices.",
                                            "device": "Create, Update and Delete devices.",
                                            "interface:read": "Read interfaces.",
                                            "interface": "Create, Update and Delete interfaces.",
                                            "site:read": "Read sites.",
                                            "site": "Create, Update and Delete sites.",
                                            "tunnel:read": "Read sites.",
                                            "tunnel": "Create, Update and Delete sites.",
                                            "user:read": "Read users.",
                                            "user": "Create, Update and Delete users.",
                                            "task:read": "Read information about tasks.",
                                            "task": "Create, Update and Delete tasks.",
                                            "self:read": "Read information about the current user.",
                                            "self": "Create, Update and Delete the current user.",
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
    try:
        data = decode(token, SECRET_KEY, [ALGORITHM])
    except Exception:
        raise InvalidTokenError
    print(UUID(data['sub']))
    return TokenData(sub=UUID(data['sub']), scopes=data['scopes'].split(), exp=data['exp'])