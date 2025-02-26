from fastapi import APIRouter, Depends, Security, status, Response
from api.main.controllers.task import TaskController
from api.main.security.authorization import authorize_user
from api.main.types.task import TaskPublic, TaskFullInput, TaskPartialInput
from api.main.types.user import UserPrivate
from typing_extensions import Annotated
from uuid import UUID


router = APIRouter(prefix="/task", tags=["task"])

controller = TaskController()


@router.get('/all', status_code=status.HTTP_200_OK, response_model=list[TaskPublic])
async def read_all_tasks(current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["task:read"])]) -> list[TaskPublic] | None:
    response: list[TaskPublic] | None = await controller.read_all()
    return response

@router.get('/{id}', status_code=status.HTTP_200_OK)
async def read_task(id: UUID,
                      current_user: Annotated[UserPrivate,
                                                    Security(authorize_user, 
                                                    scopes=["task:read"])]) -> None:
    response: TaskPublic | None = await controller.read_by_id(id=id)
    return response