from fastapi import APIRouter, Depends, Security, status, Response
from api.main.controllers.site import SiteController
from api.main.security.authorization import authorize_user
from api.main.types.site import SitePublic, SiteFullInput, SitePartialInput
from api.main.types.user import UserPrivate
from typing_extensions import Annotated
from uuid import UUID


router = APIRouter(prefix="/site", tags=["site"])

controller = SiteController()

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_site(new_site: Annotated[SiteFullInput, Depends], 
                      current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["site"])]) -> UUID | None:
    response = await controller.create(current_user=current_user, data=new_site)
    return response

@router.get('/all', status_code=status.HTTP_200_OK, response_model=list[SitePublic])
async def read_all_sites(current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["site:read"])]) -> list[SitePublic] | None:
    response: list[SitePublic] | None = await controller.read_all()
    return response

@router.get('/{id}', status_code=status.HTTP_200_OK)
async def read_site(id: UUID,
                    current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["site:read"])]) -> None:
    response: SitePublic | None = await controller.read_by_id(id=id)
    return response

@router.patch('/{id}', status_code=status.HTTP_200_OK)
async def partial_update_site(id: UUID, 
                              site_update: Annotated[SitePartialInput, Depends], 
                              current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["site"])]) -> SitePublic:
    response: SitePublic = await controller.partial_update(current_user=current_user, id=id, new_data=site_update)
    return response

@router.patch('/{id}/delete', status_code=status.HTTP_200_OK)
async def delete_site(id: UUID, current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["site"])]) -> None:
    response: SitePublic = await controller.delete(current_user=current_user, id=id)
    return response
@router.patch('/{id}/undelete', status_code=status.HTTP_200_OK)
async def undelete_site(id: UUID, current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["site"])]) -> SitePublic:
    response: SitePublic = await controller.undelete(id=id)
    return response

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def hard_delete_site(id: UUID, 
                      current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["site"])]) -> None:
    await controller.hard_delete(current_user=current_user, id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
