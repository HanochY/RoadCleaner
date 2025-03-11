from fastapi import APIRouter, Depends, Security, status, Response
from api.main.controllers.device import DeviceController
from api.main.security.authorization import authorize_user
from api.main.types.device import DevicePublic, DeviceFullInput, DevicePartialInput
from api.main.types.user import UserPrivate
from typing_extensions import Annotated
from uuid import UUID


router = APIRouter(prefix="/device", tags=["device"])

controller = DeviceController()

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_device(new_device: Annotated[DeviceFullInput, Depends], 
                        current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["device"])]) -> UUID | None:
    response = await controller.create(current_user=current_user, data=new_device)
    return response

@router.get('/all', status_code=status.HTTP_200_OK, response_model=list[DevicePublic])
async def read_all_devices(current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["device:read"])]) -> list[DevicePublic] | None:
    if current_user:
        response: list[DevicePublic] | None = await controller.read_all()
    return response

@router.get('/{id}', status_code=status.HTTP_200_OK)
async def read_device(id: UUID, 
                      current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["device:read"])]) -> None:
    if current_user:
        response: DevicePublic | None = await controller.read_by_id(id=id)
    return response

@router.patch('/{id}', status_code=status.HTTP_200_OK)
async def partial_update_device(id: UUID, device_update: Annotated[DevicePartialInput, Depends], 
                                current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["device"])]) -> DevicePublic:
    response: DevicePublic = await controller.partial_update(current_user=current_user, id=id, new_data=device_update)
    return response

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(id: UUID,
                        current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["device"])]) -> None:
    if current_user:
        await controller.delete(id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
