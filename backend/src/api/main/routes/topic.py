from fastapi import APIRouter, Depends, status, Response
from api.main.controllers.topic import TopicController
from utils.exceptions import *
from dal.schema.resources.topic import TopicPublic, TopicFullInput, TopicPartialInput
from typing_extensions import Annotated
from uuid import UUID

router = APIRouter(prefix="/topic", tags=["topic"])

controller = TopicController()

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_topic(topic: Annotated[TopicFullInput, Depends]) -> UUID | None:
    response: UUID | None = await controller.create(data=topic)
    return response
        
@router.get('/all', status_code=status.HTTP_200_OK, response_model=list[TopicPublic])
async def read_all_topics() -> list[TopicPublic]:
    response: list[TopicPublic] = await controller.read_all()
    return response

@router.patch('/{id}', status_code=status.HTTP_200_OK)
async def partial_update_topic(id: UUID, topic_update: Annotated[TopicPartialInput, Depends]) -> TopicPublic:
    response: TopicPublic = await controller.partial_update(id=id, new_data=topic_update)
    return response

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_topic(id: UUID) -> None:
    await controller.delete(id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
