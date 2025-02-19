from fastapi import APIRouter, Depends, Security, status, Response
from api.main.controllers.interface import InterfaceController
from api.main.security.authorization import authorize_user
from api.main.types.interface import InterfacePublic, InterfaceFullInput, InterfacePartialInput
from api.main.types.user import UserPrivate
from typing_extensions import Annotated
from uuid import UUID


router = APIRouter(prefix="/interface", tags=["interface"])

controller = InterfaceController()

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_interface(new_interface: Annotated[InterfaceFullInput, Depends], 
                           current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["interface"])]) -> UUID | None:
    response = await controller.create(current_user=current_user, data=new_interface)
    return response

@router.get('/{id}', status_code=status.HTTP_200_OK)
async def read_interface(id: UUID, 
                         current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["interface:read"])]) -> None:
    response: InterfacePublic | None = await controller.read_by_id(current_user=current_user, id=id)
    return response

@router.get('/all', status_code=status.HTTP_200_OK, response_model=InterfacePublic)
async def read_all_interfaces(current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["interface:read"])]) -> list[InterfacePublic] | None:
    response: list[InterfacePublic] | None = await controller.read_all(current_user=current_user)
    return response

@router.patch('/{id}', status_code=status.HTTP_200_OK)
async def partial_update_interface(id: UUID, 
                                   interface_update: Annotated[InterfacePartialInput, Depends], 
                                   current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["interface"])]) -> InterfacePublic:
    response: InterfacePublic = await controller.partial_update(current_user=current_user, id=id, new_data=interface_update)
    return response

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_interface(id: UUID, 
                           current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["interface"])]) -> None:
    await controller.delete(current_user=current_user, id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
