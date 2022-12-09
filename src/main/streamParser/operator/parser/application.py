import traceback

from src.main.streamParser.config import Settings
from pydantic.error_wrappers import ValidationError
from src.main.streamParser.exception import StreamParserException
from src.main.streamParser.operator.parser.model import ParseFlowRequestInfo
from src.main.streamParser.base.application import Application as BaseApplication
from src.main.streamParser.parser.n8n.workflow_entity.application import get_app as get_n8n_parser_app


class Application(BaseApplication):
    @staticmethod
    def _parse_stream(request_info: ParseFlowRequestInfo):
        try:
            app = get_n8n_parser_app(request_info.dict())
        except ValidationError as _e:
            raise StreamParserException("validate model error: {}".format(traceback.format_exc()), error_code=422)
        return app.flow

    def parse_stream(self, request_info: ParseFlowRequestInfo):
        result = self._parse_stream(request_info)
        return {"result": result}


application = Application(Settings)
