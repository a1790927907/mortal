from fastapi import APIRouter, Response
from src.main.streamParser.api.base.app import process_request
from src.main.streamParser.api.n8n.model import ParsedFlowResponse
from src.main.streamParser.operator.parser.model import ParseFlowRequestInfo
from src.main.streamParser.operator.parser.application import application as parser_app


router_app = APIRouter(prefix="/stream/n8n", tags=["n8nParser"])


@router_app.post(
    "/parse", response_model=ParsedFlowResponse, name="解析n8n流", description="解析n8n流 用于存储"
)
def parse_stream(response: Response, request_info: ParseFlowRequestInfo):
    result = process_request(response, func=parser_app.parse_stream, func_params={"request_info": request_info})
    return result
