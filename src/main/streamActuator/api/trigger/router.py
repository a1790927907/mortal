from fastapi import APIRouter, Response
from src.main.streamActuator.api.base.app import process_request
from src.main.streamActuator.integration.model import RequestInfo
from src.main.streamActuator.api.trigger.model import TriggerConnectionResponse
from src.main.streamActuator.integration.application import application as trigger_integration_app


router_app = APIRouter(prefix="/stream/trigger", tags=["trigger"])


@router_app.post(
    "/connection", response_model=TriggerConnectionResponse, name="触发一个connection(flow)",
    description="触发一个connection(flow)"
)
async def trigger_connection(
        request_info: RequestInfo,
        response: Response
):
    coroutine = trigger_integration_app.schedule_connection(request_info)
    result = await process_request(response, coroutine=coroutine)
    return result
