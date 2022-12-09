from typing import Callable
from fastapi import Response
from src.main.utils.logger import logger
from src.main.streamParser.exception import StreamParserException


def process_request(response: Response, *, func: Callable, func_params: dict):
    try:
        result = func(**func_params)
        return result
    except StreamParserException as e:
        message = e.message
        logger.error(e.message)
        response.status_code = e.error_code
    except Exception as e:
        logger.exception(e)
        response.status_code = 500
        message = repr(e)
    return {"message": message}
