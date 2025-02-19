from fastapi import APIRouter, Depends, Security, status, Response
from api.main.controllers.user import UserController
from api.main.security.authorization import authorize_user
from api.main.types.user import UserPublic, UserPrivate, UserFullInput, UserPartialInput
from typing_extensions import Annotated
from uuid import UUID


router = APIRouter(prefix="/user", tags=["user"])

controller = UserController()

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(new_user: Annotated[UserFullInput, Depends], 
                      current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["user"])]) -> UUID | None:
    response = await controller.create(current_user=current_user, data=new_user)
    return response

@router.get('/{id}', status_code=status.HTTP_200_OK)
async def read_user(id: UUID,
                    current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["user:read"])]) -> None:
    response: UserPublic | None = await controller.read_by_id(current_user=current_user, id=id)
    return response
    
@router.get('/me', status_code=status.HTTP_200_OK, response_model=UserPublic)
async def read_current_user(current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["self"])]) -> UserPublic:
    return current_user


    
@router.get('/all', status_code=status.HTTP_200_OK, response_model=UserPublic)
async def read_all_users(current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["user:read"])]) -> list[UserPublic] | None:
    response: list[UserPublic] | None = await controller.read_all(current_user=current_user)
    return response

@router.patch('/{id}', status_code=status.HTTP_200_OK)
async def partial_update_user(id: UUID,
                              user_update: Annotated[UserPartialInput, Depends], 
                              current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["user"])]) -> UserPublic:
    response: UserPublic = await controller.partial_update(current_user=current_user, id=id, new_data=user_update)
    return response

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: UUID,
                      current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["user"])]) -> None:
    await controller.delete(current_user=current_user, id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
