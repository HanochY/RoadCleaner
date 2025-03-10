from fastapi import APIRouter, Depends, Security, status, Response
from api.main.controllers.tunnel.juniper import JuniperTunnelController
from api.main.security.authorization import authorize_user
from api.main.types.tunnel.juniper import JuniperTunnelPublic, JuniperTunnelFullInput, JuniperTunnelPartialInput
from api.main.types.user import UserPrivate
from typing_extensions import Annotated
from uuid import UUID


router = APIRouter(prefix="/juniper", tags=["juniper"])

controller = JuniperTunnelController()

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_juniper_tunnel(new_juniper_tunnel: Annotated[JuniperTunnelFullInput, Depends], 
                        current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["tunnel"])]) -> UUID | None:
    response = await controller.create(current_user=current_user, data=new_juniper_tunnel)
    return response

@router.get('/all', status_code=status.HTTP_200_OK, response_model=list[JuniperTunnelPublic])
async def read_all_juniper_tunnels(current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["tunnel:read"])]) -> list[JuniperTunnelPublic] | None:
    response: list[JuniperTunnelPublic] | None = await controller.read_all()
    return response

@router.get('/{id}', status_code=status.HTTP_200_OK)
async def read_juniper_tunnel(id: UUID,
                      current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["tunnel:read"])]) -> None:
    response: JuniperTunnelPublic | None = await controller.read_by_id(id=id)
    return response

@router.patch('/{id}', status_code=status.HTTP_200_OK)
async def partial_update_juniper_tunnel(id: UUID, 
                                juniper_tunnel_update: Annotated[JuniperTunnelPartialInput, Depends], 
                                current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["tunnel"])]) -> JuniperTunnelPublic:
    response: JuniperTunnelPublic = await controller.partial_update(current_user=current_user, id=id, new_data=juniper_tunnel_update)
    return response

@router.patch('/{id}/delete', status_code=status.HTTP_200_OK)
async def delete_juniper_tunnel(id: UUID, current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["tunnel"])]) -> None:
    response: JuniperTunnelPublic = await controller.delete(current_user=current_user, id=id)
    return response

@router.patch('/{id}/undelete', status_code=status.HTTP_200_OK)
async def undelete_juniper_tunnel(id: UUID, current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["tunnel"])]) -> JuniperTunnelPublic:
    response: JuniperTunnelPublic = await controller.undelete(id=id)
    return response


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def hard_delete_juniper_tunnel(id: UUID, 
                        current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["tunnel"])]) -> None:
    await controller.hard_delete(current_user=current_user, id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
