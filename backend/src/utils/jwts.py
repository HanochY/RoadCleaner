from datetime import datetime, timedelta, timezone

import jwt
from jwt import InvalidTokenError

from api.main.security.tokens import TokenData

    
def encode_jwt(data: TokenData,  secret_key: str, algorithm: str) -> str:
    token = jwt.encode(data, secret_key, algorithm=algorithm)
    return token


async def decode_jwt(token: str, secret_key: str, algorithm: str) -> str:
    try:
        data: TokenData = jwt.decode(token, secret_key, algorithms=[algorithm])
    except InvalidTokenError:
        raise InvalidTokenError("Invalid token")
    return data