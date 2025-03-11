from fastapi import APIRouter, Depends, Security, status, Response
from api.main.controllers.tunnel.cisco import CiscoTunnelController
from api.main.security.authorization import authorize_user
from api.main.types.tunnel.cisco import CiscoTunnelPublic, CiscoTunnelFullInput, CiscoTunnelPartialInput
from api.main.types.user import UserPrivate
from typing_extensions import Annotated
from uuid import UUID


router = APIRouter(prefix="/cisco", tags=["cisco"])

controller = CiscoTunnelController()

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_cisco_tunnel(new_cisco_tunnel: Annotated[CiscoTunnelFullInput, Depends], 
                        current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["tunnel"])]) -> UUID | None:
    response = await controller.create(current_user=current_user, data=new_cisco_tunnel)
    return response

@router.get('/all', status_code=status.HTTP_200_OK, response_model=list[CiscoTunnelPublic])
async def read_all_cisco_tunnels(current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["tunnel:read"])]) -> list[CiscoTunnelPublic] | None:
    response: list[CiscoTunnelPublic] | None = await controller.read_all()
    return response

@router.get('/{id}', status_code=status.HTTP_200_OK)
async def read_cisco_tunnel(id: UUID,
                      current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["tunnel:read"])]) -> None:
    response: CiscoTunnelPublic | None = await controller.read_by_id(id=id)
    return response

@router.patch('/{id}', status_code=status.HTTP_200_OK)
async def partial_update_cisco_tunnel(id: UUID, 
                                cisco_tunnel_update: Annotated[CiscoTunnelPartialInput, Depends], 
                                current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["tunnel"])]) -> CiscoTunnelPublic:
    response: CiscoTunnelPublic = await controller.partial_update(current_user=current_user, id=id, new_data=cisco_tunnel_update)
    return response

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_cisco_tunnel(id: UUID, 
                        current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["tunnel"])]) -> None:
    await controller.delete(id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
