import time
import asyncio
import dateutil.parser as date_parser

from datetime import datetime
from src.main.utils.time_utils import get_now
from src.main.streamActuator.model import Task
from src.main.streamActuator.config import Settings
from src.main.streamActuator.exception import StreamActuatorException
from src.main.streamActuator.executor.base.application import Application as BaseApplication


class Application(BaseApplication):
    @staticmethod
    async def execute_specific_time_task(datetime_string: str):
        fmt = "%Y-%d-%m %H:%M:%S"
        waited_time = date_parser.parse(datetime_string).strftime(fmt)
        waited_time = datetime.strptime(waited_time, fmt)
        while waited_time >= get_now(fmt):
            await asyncio.sleep(2)

    @staticmethod
    async def execute_after_time_task(interval: float, units: str):
        units_mappings = {
            "seconds": 1,
            "minutes": 60,
            "hours": 60 * 60,
            "days": 24 * 60 * 60
        }
        interval_time = interval * (units_mappings.get(units) or 1)
        await asyncio.sleep(interval_time)

    async def execute_task(self) -> bool:
        now = time.time()
        parameters = self.task.payload.parameters
        resume = parameters.get("resume") or "timeInterval"
        if resume == "timeInterval":
            date_time = parameters["dateTime"]
            date_time = self._parse_raw_expressions(date_time)
            await self.execute_specific_time_task(date_time)
        elif resume == "timeInterval":
            amount, unit = parameters.get("amount") or 1., parameters.get("unit") or "hours"
            amount = self._parse_raw_expressions(amount) if isinstance(amount, str) else amount
            unit = self._parse_raw_expressions(unit) if isinstance(unit, str) else unit
            await self.execute_after_time_task(amount, unit)
        else:
            raise StreamActuatorException("invalid resume option: {}".format(resume), error_code=400)
        self.set_result({"value": True, "executeTime": time.time() - now})
        return True


def get_app(task: dict, context: dict):
    return Application(Settings, Task(**task), context)
