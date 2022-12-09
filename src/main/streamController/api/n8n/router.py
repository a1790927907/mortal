from fastapi import APIRouter, Response, Query
from src.main.streamController.config import Settings
from src.main.streamController.api.base.app import process_request
from src.main.streamController.api.n8n.model import SaveConnectionFromN8NResponse
from src.main.streamController.operator.n8n.application import Application as N8NApplication


router_app = APIRouter(prefix="/stream/reference/n8n", tags=["n8n"])
app = N8NApplication(Settings)


@router_app.post(
    "/save", response_model=SaveConnectionFromN8NResponse, name="通过n8n的workflow转换存储",
    description="通过n8n的workflow转换存储"
)
async def save_stream_by_n8n_id(
    response: Response, reference_id: int = Query(..., description="reference id", example="xxx")
):
    result = await process_request(response, coroutine=app.save_stream_by_reference_id(reference_id))
    return result
