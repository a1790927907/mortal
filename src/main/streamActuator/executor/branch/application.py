import re
import time
import dateutil.parser as date_parser

from typing import Dict, List, Callable
from src.main.streamActuator.model import Task
from src.main.streamActuator.config import Settings
from src.main.streamActuator.exception import StreamActuatorException
from src.main.streamActuator.executor.base.application import Application as BaseApplication


class Application(BaseApplication):
    def process_boolean_condition(self, condition: dict) -> Callable[[], bool]:
        op = condition.get("operation") or "equal"
        value1, value2 = condition.get("value1") or False, condition.get("value2") or False
        value1 = self._parse_raw_expressions(value1) if isinstance(value1, str) else value1
        value2 = self._parse_raw_expressions(value2) if isinstance(value2, str) else value2
        value1, value2 = bool(value1), bool(value2)
        if op == "notEqual":
            return lambda: value1 is value2
        else:
            return lambda: value1 is not value2

    def process_datetime_condition(self, condition: dict) -> Callable[[], bool]:
        def parse_date(text: str):
            try:
                return date_parser.parse(text)
            except Exception as _e:
                return ""
        op = condition.get("operation") or "after"
        value1, value2 = condition.get("value1") or "", condition.get("value2") or ""
        value1 = self._parse_raw_expressions(value1) if isinstance(value1, str) else value1
        value2 = self._parse_raw_expressions(value2) if isinstance(value2, str) else value2
        value1, value2 = parse_date(value1), parse_date(value2)
        if type(value1) != type(value2):
            return lambda: False
        if op == "after":
            return lambda: value1 >= value2
        else:
            return lambda: value1 <= value2

    def process_number_condition(self, condition: dict) -> Callable[[], bool]:
        def parse_number(source):
            try:
                return float(source)
            except Exception as _e:
                return None

        op = condition.get("operation") or "smaller"
        value1, value2 = condition.get("value1") or 0, condition.get("value2") or 0
        value1 = self._parse_raw_expressions(value1) if isinstance(value1, str) else value1
        value2 = self._parse_raw_expressions(value2) if isinstance(value2, str) else value2
        value1, value2 = parse_number(value1) or 0, parse_number(value2) or 0
        if op == "smaller":
            return lambda: value1 < value2
        elif op == "smallerEqual":
            return lambda: value1 <= value2
        elif op == "equal":
            return lambda: value1 == value2
        elif op == "notEqual":
            return lambda: value1 != value2
        elif op == "larger":
            return lambda: value1 > value2
        elif op == "largerEqual":
            return lambda: value1 >= value2
        elif op == "isEmpty" or op == "isNotEmpty":
            return lambda: bool(value1)
        raise StreamActuatorException("invalid number operator: {}".format(op), error_code=400)

    def process_string_condition(self, condition: dict) -> Callable[[], bool]:
        op = condition.get("operation") or "equal"
        value1, value2 = condition.get("value1") or "", condition.get("value2") or ""
        value1 = self._parse_raw_expressions(value1) if isinstance(value1, str) else value1
        value2 = self._parse_raw_expressions(value2) if isinstance(value2, str) else value2
        value1, value2 = str(value1) if value1 is not None else "", str(value2) if value2 is not None else ""
        if op == "contains":
            return lambda: value2 in value1
        elif op == "notContains":
            return lambda: value2 not in value1
        elif op == "endsWith":
            return lambda: value1.endswith(value2)
        elif op == "notEndsWith":
            return lambda: not value1.endswith(value2)
        elif op == "equal":
            return lambda: value1 == value2
        elif op == "notEqual":
            return lambda: value1 != value2
        elif op == "regex":
            return lambda: bool(re.search(value2, value1))
        elif op == "notRegex":
            return lambda: not bool(re.search(value2, value1))
        elif op == "startsWith":
            return lambda: value1.startswith(value2)
        elif op == "notStartsWith":
            return lambda: not value1.startswith(value2)
        elif op == "isEmpty" or op == "isNotEmpty":
            return lambda: bool(value1)
        raise StreamActuatorException("invalid string operator: {}".format(op), error_code=400)

    def process_parameters(self, parameters: dict):
        conditions: Dict[str, List[dict]] = parameters.get("conditions") or []
        result: List[Callable[[], bool]] = []
        for condition_name, condition in conditions.items():
            for condition_info in condition:
                if condition_name == "boolean":
                    result.append(self.process_boolean_condition(condition_info))
                elif condition_name == "dateTime":
                    result.append(self.process_datetime_condition(condition_info))
                elif condition_name == "number":
                    result.append(self.process_number_condition(condition_info))
                elif condition_name == "string":
                    result.append(self.process_string_condition(condition_info))
        return result

    async def _execute_task(self) -> bool:
        now = time.time()
        conditions_functions = self.process_parameters(self.task.payload.parameters)
        combine = self.task.payload.parameters.get("combineOperation") or "all"
        result = list(map(lambda x: x(), conditions_functions))
        spend = time.time() - now
        if combine == "all":
            result = all(result)
            self.set_result({"value": result, "executeTime": spend})
            return result
        result = any(result)
        self.set_result({"value": result, "executeTime": spend})
        return result

    async def execute_task(self) -> bool:
        now = time.time()
        try:
            result = await self._execute_task()
            return result
        except Exception as e:
            self.set_result({"value": None, "executeTime": time.time() - now})
            raise e


def get_app(task: dict, context: dict):
    return Application(Settings, Task(**task), context)


if __name__ == '__main__':
    import json
    import asyncio
    with open("/Users/zyh/mortal/src/main/streamActuator/executor/test/data/processed_flow.json") as f:
        print(asyncio.run(
            get_app(json.load(f)["nodes"][8], {"Start": {"openId": "sadj"}}).execute_task()
        ))
