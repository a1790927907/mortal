from typing import Coroutine
from fastapi import Response
from src.main.utils.logger import logger
from src.main.streamStorage.exception import StreamStorageException


async def process_request(response: Response, coroutine: Coroutine):
    try:
        result = await coroutine
        return result
    except StreamStorageException as e:
        message = e.message
        logger.error(e.message)
        response.status_code = e.error_code
    except Exception as e:
        message = repr(e)
        logger.exception(e)
        response.status_code = 500
    return {"message": message}
