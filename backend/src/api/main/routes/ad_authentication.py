from fastapi import APIRouter, Depends

from api.main.controllers.authentication import AuthenticationController
from api.main.security.tokens import FastAPIBearerToken


router = APIRouter(prefix="/ad-auth", tags=["ad-auth"])
controller = AuthenticationController()

@router.post("/token")
async def generate_token() -> FastAPIBearerToken:
    pass