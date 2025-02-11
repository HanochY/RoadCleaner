from fastapi import APIRouter, Depends, status, Response
from api.main.controllers.comment import CommentController
from utils.exceptions import *
from dal.schema.resources.comment import CommentPublic, CommentFullInput, CommentPartialInput
from typing_extensions import Annotated
from uuid import UUID

router = APIRouter(prefix="/comment", tags=["comment"])

controller = CommentController()

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_comment(comment: Annotated[CommentFullInput, Depends]) -> UUID:
    response: UUID = await controller.create(data=comment)
    return response
        
@router.get('/all', status_code=status.HTTP_200_OK, response_model=list[CommentPublic])
async def read_all_comments() -> list[CommentPublic]:
    response: list[CommentPublic] | None = await controller.read_all()
    return response

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=CommentPublic)
async def read_comment_by_id() -> list[CommentPublic]:
    response: CommentPublic | None = await controller.read_by_id()
    return response
        
@router.patch('/{id}', status_code=status.HTTP_200_OK)
async def partial_update_comment(id: UUID, comment_update: Annotated[CommentPartialInput, Depends]) -> CommentPublic:
    response: CommentPublic = await controller.partial_update(id=id, new_data=comment_update)
    return response

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(id: UUID) -> Response:
    await controller.delete(id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
