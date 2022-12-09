from fastapi import Response
from typing import Coroutine
from src.main.utils.logger import logger
from src.main.streamController.exception import StreamControllerException


async def process_request(response: Response, *, coroutine: Coroutine):
    try:
        result = await coroutine
        return result
    except StreamControllerException as e:
        message = e.message
        logger.error(e.message)
        response.status_code = e.error_code
    except Exception as e:
        logger.exception(e)
        response.status_code = 500
        message = repr(e)
    return {"message": message}
