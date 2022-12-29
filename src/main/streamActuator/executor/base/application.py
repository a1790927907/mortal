import re
import json

from copy import deepcopy
from typing import Type, Optional
from jinja2.runtime import Undefined
from jinja2.nativetypes import NativeTemplate
from src.main.streamActuator.model import Task
from src.main.streamActuator.config import Settings
from src.main.streamActuator.executor.model import ExecutorResult
from src.main.streamActuator.base.application import Application as BaseApplication


class Application(BaseApplication):
    def __init__(self, settings: Type[Settings], task: Task, context: dict):
        super().__init__(settings)
        self.task = task
        self.context = context
        self._result = None
        self.error_message: Optional[str] = None
        self.retry_time: int = 0

    def merge_result(self, value: dict):
        if self._result is None:
            self._result = ExecutorResult(**value)
        else:
            _result_dict = self._result.dict()
            _result_dict.update(value)
            self._result = ExecutorResult(**_result_dict)

    def set_result(self, value: dict):
        self._result = ExecutorResult(**value)

    @property
    def result(self) -> Optional[dict]:
        return self._result.dict() if self._result is not None else None

    @staticmethod
    def render(text: str, **kwargs):
        try:
            return NativeTemplate(text).render(**kwargs)
        except Exception as _e:
            return None

    def _parse_expressions(self, expression: str):
        template = expression.replace("$node", "ctx_zyh", 1).replace(".json", "['value']", 1).\
            replace(".kwargs", "['extraValue']")
        parsed_result = self.render(template, ctx_zyh=self.context)
        parsed_result = None if isinstance(parsed_result, Undefined) else parsed_result
        return parsed_result

    def _parse_raw_expressions(self, raw: str):
        # 针对字符串中的所有表达式解析
        raw = raw.replace("=", "", 1) if raw.startswith("=") else raw
        expression = re.compile(r"\{\{.*?\}\}")
        expression_string_list = expression.findall(raw)
        if len(expression_string_list) == 1 and expression_string_list[0] == raw:
            return self._parse_expressions(expression_string_list[0])
        for expression_string in expression_string_list:
            parsed_result = self._parse_expressions(expression_string)
            if isinstance(parsed_result, str) or isinstance(parsed_result, int) or isinstance(parsed_result, float):
                raw = raw.replace(expression_string, str(parsed_result), 1)
            elif parsed_result is None:
                raw = raw.replace(expression_string, "null", 1)
            elif isinstance(parsed_result, bool):
                raw = raw.replace(expression_string, json.dumps(raw, ensure_ascii=False), 1)
            else:
                raw = raw.replace(expression_string, "[object]", 1)
        return raw

    def _parse_json_string_expressions(self, json_string: str):
        # 针对 json string 中的表达式解析
        json_string = json_string.replace("=", "", 1) if json_string.startswith("=") else json_string
        expression = re.compile(r"\{\{.*?\}\}")
        expression_string_list = expression.findall(json_string)
        for expression_string in expression_string_list:
            parsed_result = self._parse_expressions(expression_string)
            if isinstance(parsed_result, str):
                json_string = json_string.replace(expression_string, parsed_result, 1)
            elif parsed_result is None or isinstance(parsed_result, int) or isinstance(parsed_result, float):
                new_expression_string = '"{}"'.format(expression_string)
                replaced_value = str(parsed_result) if parsed_result is not None else "null"
                if new_expression_string in json_string and json_string.index(new_expression_string) == \
                        json_string.index(expression_string) - 1:
                    json_string = json_string.replace(new_expression_string, replaced_value, 1)
                else:
                    json_string = json_string.replace(expression_string, replaced_value, 1)
            else:
                json_string = json_string.replace(expression_string, json.dumps(parsed_result, ensure_ascii=False), 1)
        return json_string

    def _parse_dict_key(self, obj: dict):
        result = deepcopy(obj)
        for key in result.keys():
            obj.pop(key)
            obj[self._parse_raw_expressions(key)] = result[key]

    def _parse_dict(self, obj: dict):
        self._parse_dict_key(obj)
        for key, value in obj.items():
            if isinstance(value, dict):
                self._parse_dict(value)
            elif isinstance(value, list):
                for index, v in enumerate(value):
                    if isinstance(v, dict):
                        self._parse_dict(v)
                    elif isinstance(v, list):
                        self._parse_dict({"foo": v})
                    elif isinstance(v, str):
                        value[index] = self._parse_raw_expressions(v)
            elif isinstance(value, str):
                obj[key] = self._parse_raw_expressions(value)
        return obj

    async def execute_task(self) -> bool:
        raise NotImplementedError


if __name__ == '__main__':
    print(
        Application(Settings, ..., {"data": {"a": {"b": 1}, "c": "fasf", "e": [1, "2aa"]}})._parse_raw_expressions(
            '=hehe{{$node["data"].json["c"]}}12345'
        )
    )
    print(
        Application(Settings, ..., {"data": {"a": {"b": 1}, "c": "100", "e": [1, "2aa"]}})._parse_json_string_expressions(
            '={"data": {{$node["data"].json["a"]}}, "meta": {{$node["data"].json["a"]["b"]}}, '
            '"hehe": "{{$node["data"].json["c"]}}", "tex": "12121"}'
        )
    )
