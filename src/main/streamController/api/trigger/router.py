from fastapi import APIRouter, Response
from src.main.streamController.config import Settings
from src.main.streamController.api.base.app import process_request
from src.main.streamController.api.trigger.model import TriggerConnectionResponse
from src.main.streamController.operator.trigger.model import RequestInfo as TriggerRequestInfo
from src.main.streamController.operator.trigger.application import Application as TriggerApplication


router_app = APIRouter(prefix="/stream/reference/trigger", tags=["trigger"])
app = TriggerApplication(Settings)


@router_app.post(
    "/connection", response_model=TriggerConnectionResponse, description="根据connection触发工作流",
    name="根据connection触发工作流"
)
async def trigger_connection(response: Response, request_info: TriggerRequestInfo):
    result = await process_request(response, coroutine=app.trigger_connection(request_info))
    return result
