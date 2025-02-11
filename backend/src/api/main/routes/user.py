from fastapi import APIRouter, Depends, Security, status, Response
from api.main.controllers.user import UserController
from api.main.controllers.authentication import AuthenticationController
from utils.exceptions import *
from dal.schema.resources.user import UserPublic, UserFullInput, UserPartialInput
from typing_extensions import Annotated
from uuid import UUID

router = APIRouter(prefix="/user", tags=["user"])

controller = UserController()
auth_controller = AuthenticationController() # to be moved

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(user: Annotated[UserFullInput, Depends]) -> UUID | None:
    response = await controller.create(data=user)
    return response

@router.get('/me', status_code=status.HTTP_200_OK, response_model=UserPublic)
async def read_current_user(current_user: Annotated[UserPublic,
                                                    Security(auth_controller.get_current_user, 
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
