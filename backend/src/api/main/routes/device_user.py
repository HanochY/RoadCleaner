from fastapi import APIRouter, Depends, Security, status, Response
from api.main.controllers.device_user import DeviceUserController
from api.main.security.authorization import authorize_user
from api.main.types.device_user import DeviceUserPublic, DeviceUserFullInput, DeviceUserPartialInput
from api.main.types.user import UserPrivate
from typing_extensions import Annotated
from uuid import UUID


router = APIRouter(prefix="/device_user", tags=["device_user"])

controller = DeviceUserController()

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_device_user(new_device_user: Annotated[DeviceUserFullInput, Depends], 
                        current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["device_user"])]) -> UUID | None:
    response = await controller.create(current_user=current_user, data=new_device_user)
    return response

@router.get('/all', status_code=status.HTTP_200_OK, response_model=list[DeviceUserPublic])
async def read_all_device_users(current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["device_user:read"])]) -> list[DeviceUserPublic] | None:
    if current_user:
        response: list[DeviceUserPublic] | None = await controller.read_all()
    return response

@router.get('/{id}', status_code=status.HTTP_200_OK)
async def read_device_user(id: UUID, 
                      current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["device_user:read"])]) -> None:
    if current_user:
        response: DeviceUserPublic | None = await controller.read_by_id(id=id)
    return response

@router.patch('/{id}', status_code=status.HTTP_200_OK)
async def partial_update_device_user(id: UUID, device_user_update: Annotated[DeviceUserPartialInput, Depends], 
                                current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["device_user"])]) -> DeviceUserPublic:
    response: DeviceUserPublic = await controller.partial_update(current_user=current_user, id=id, new_data=device_user_update)
    return response

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_device_user(id: UUID,
                        current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["device_user"])]) -> None:
    if current_user:
        await controller.delete(id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
