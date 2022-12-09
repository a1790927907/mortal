from fastapi import Response
from typing import Coroutine
from src.main.utils.logger import logger
from src.main.monitor.exception import MonitorException


async def process_request(response: Response, *, coroutine: Coroutine):
    try:
        result = await coroutine
        return result
    except MonitorException as e:
        message = e.message
        response.status_code = e.error_code
        logger.error(message)
    except Exception as e:
        logger.exception(e)
        message = repr(e)
        response.status_code = 500
    return {"message": message}
