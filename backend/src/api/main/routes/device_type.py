from fastapi import APIRouter, Depends, Security, status, Response
from api.main.controllers.device_type import DeviceTypeController
from api.main.security.authorization import authorize_user
from api.main.types.device_type import DeviceTypePublic, DeviceTypeFullInput, DeviceTypePartialInput
from api.main.types.user import UserPrivate
from typing_extensions import Annotated
from uuid import UUID


router = APIRouter(prefix="/device_type", tags=["device_type"])

controller = DeviceTypeController()

@router.get('/all', status_code=status.HTTP_200_OK, response_model=list[DeviceTypePublic])
async def read_all_device_types(current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["device_type:read"])]) -> list[DeviceTypePublic] | None:
    response: list[DeviceTypePublic] | None = await controller.read_all()
    return response

@router.get('/{id}', status_code=status.HTTP_200_OK)
async def read_device_type(id: UUID,
                           current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["device_type:read"])]) -> None:
    response: DeviceTypePublic | None = await controller.read_by_id(id=id)
    return response

