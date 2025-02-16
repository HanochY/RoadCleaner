from fastapi import APIRouter, Depends, Security, status, Response
from api.main.controllers.user import UserController
from api.main.security.authorization import AuthorizationManager
from utils.exceptions import *
from api.main.types.user import UserPublic, UserFullInput, UserPartialInput
from typing_extensions import Annotated
from uuid import UUID
from api.main.security.tokens import (
    oauth2_scheme
)

router = APIRouter(prefix="/user", tags=["user"])

controller = UserController()
authorization_manager = AuthorizationManager()

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(new_user: Annotated[UserFullInput, Depends]) -> UUID | None:
    print('a')
    response = await controller.create(data=new_user)
    return response

@router.get('/me', status_code=status.HTTP_200_OK, response_model=UserPublic)
async def read_current_user(current_user: Annotated[UserPublic,
                                                    Security(authorization_manager.authorize_user, 
                                                    scopes=["self"])]) -> UserPublic:
    return current_user

@router.get('/all', status_code=status.HTTP_200_OK, response_model=UserPublic)
async def read_all_users() -> list[UserPublic] | None:
    response: list[UserPublic] | None = await controller.read_all()
    return response

@router.patch('/{id}', status_code=status.HTTP_200_OK)
async def partial_update_user(id: UUID, user_update: Annotated[UserPartialInput, Depends]) -> UserPublic:
    response: UserPublic = await controller.partial_update(id=id, new_data=user_update)
    return response

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: UUID) -> None:
    await controller.delete(id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
