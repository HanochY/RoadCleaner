from fastapi import APIRouter, Depends, Security, status, Response
from api.main.controllers.tunnel import TunnelController
from api.main.security.authorization import authorize_user
from api.main.types.tunnel import TunnelPublic, TunnelFullInput, TunnelPartialInput
from api.main.types.user import UserPrivate
from typing_extensions import Annotated
from uuid import UUID


router = APIRouter(prefix="/tunnel", tags=["tunnel"])

controller = TunnelController()

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_tunnel(new_tunnel: Annotated[TunnelFullInput, Depends], 
                        current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["tunnel"])]) -> UUID | None:
    response = await controller.create(current_user=current_user, data=new_tunnel)
    return response

@router.get('/{id}', status_code=status.HTTP_200_OK)
async def read_tunnel(id: UUID,
                      current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["tunnel:read"])]) -> None:
    response: TunnelPublic | None = await controller.read_by_id(current_user=current_user, id=id)
    return response

@router.get('/all', status_code=status.HTTP_200_OK, response_model=TunnelPublic)
async def read_all_tunnels(current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["tunnel:read"])]) -> list[TunnelPublic] | None:
    response: list[TunnelPublic] | None = await controller.read_all(current_user=current_user)
    return response

@router.patch('/{id}', status_code=status.HTTP_200_OK)
async def partial_update_tunnel(id: UUID, 
                                tunnel_update: Annotated[TunnelPartialInput, Depends], 
                                current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["tunnel"])]) -> TunnelPublic:
    response: TunnelPublic = await controller.partial_update(current_user=current_user, id=id, new_data=tunnel_update)
    return response

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_tunnel(id: UUID, 
                        current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["tunnel"])]) -> None:
    await controller.delete(current_user=current_user, id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
