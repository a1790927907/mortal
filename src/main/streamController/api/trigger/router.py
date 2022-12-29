from fastapi import APIRouter, Response
from src.main.streamController.config import Settings
from src.main.streamController.api.base.app import process_request
from src.main.streamController.api.trigger.model import TriggerConnectionResponse
from src.main.streamController.operator.trigger.application import Application as TriggerApplication
from src.main.streamController.operator.trigger.model import RequestInfo as TriggerRequestInfo, \
    RestartTasksRunRequestInfo


router_app = APIRouter(prefix="/stream/reference/trigger", tags=["trigger"])
app = TriggerApplication(Settings)


@router_app.post(
    "/connection", response_model=TriggerConnectionResponse, description="根据connection触发工作流",
    name="根据connection触发工作流"
)
async def trigger_connection(response: Response, request_info: TriggerRequestInfo):
    if request_info.asynchronous:
        result = await process_request(response, coroutine=app.trigger_connection_asynchronous(request_info))
    else:
        result = await process_request(response, coroutine=app.trigger_connection(request_info))
    return result


@router_app.post(
    "/reconstruct/tasksRun", response_model=TriggerConnectionResponse, description="根据tasks run id重启一个任务",
    name="根据tasks run id重启一个任务"
)
async def restart_tasks_run(response: Response, request_info: RestartTasksRunRequestInfo):
    result = await process_request(response, coroutine=app.restart_tasks_run(request_info))
    return result
