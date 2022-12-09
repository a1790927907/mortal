from fastapi import Response, APIRouter, Path
from src.main.streamController.config import Settings
from src.main.streamController.api.base.app import process_request
from src.main.streamController.api.loader.task.model import TaskResponse
from src.main.streamController.operator.loader.tasks.application import Application


router_app = APIRouter(prefix="/stream/reference/tasks", tags=["tasks"])
app = Application(Settings)


@router_app.get(
    "/condition/connection/{connection_id}", response_model=TaskResponse, name="根据connection id获取对应tasks",
    description="根据connection id获取对应tasks"
)
async def get_tasks_by_connection_id(
        response: Response,
        connection_id: str = Path(..., description="connection id", example="xxx")
):
    result = await process_request(response, coroutine=app.get_tasks_by_connection_id(connection_id))
    return result
