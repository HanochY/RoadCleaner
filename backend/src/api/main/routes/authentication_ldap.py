from fastapi import APIRouter, Depends, status
from api.main.controllers.authentication import AuthenticationController
from api.main.security.tokens import OAuthBearerToken

router = APIRouter(prefix="/ad-auth", tags=["ad-auth"])
controller = AuthenticationController()

@router.post("/token", status_code=status.HTTP_200_OK)
async def generate_token() -> OAuthBearerToken:
    pass