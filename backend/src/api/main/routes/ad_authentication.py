from fastapi import APIRouter, Depends

from api.main.controllers.authentication import AuthenticationController
from api.main.security.tokens import FastAPIBearerToken


router = APIRouter(prefix="/auth", tags=["auth"])
controller = AuthenticationController()

@router.post("/token")
async def generate_token(token: FastAPIBearerToken = 
                      Depends(controller.authenticate_for_access_token)) -> FastAPIBearerToken:
    return token