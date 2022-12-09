from fastapi import APIRouter, Response, Path
from src.main.streamController.config import Settings
from src.main.streamController.api.base.app import process_request
from src.main.streamController.operator.loader.monitor.application import Application
from src.main.streamController.api.loader.monitor.model import TaskStatusLoadedResponse


router_app = APIRouter(prefix="/stream/reference/monitor", tags=["monitor"])
app = Application(Settings)


@router_app.get(
    "/taskStatus/condition/tasksRun/{tasks_run_id}", response_model=TaskStatusLoadedResponse,
    description="根据tasks run id获取对应的task status记录", name="根据tasks run id获取对应的task status记录"
)
async def get_task_status_by_tasks_run_id(
        response: Response,
        tasks_run_id: str = Path(..., description="tasks run id", example="xxx")
):
    result = await process_request(response, coroutine=app.get_task_status_by_tasks_run_id(tasks_run_id))
    return result
