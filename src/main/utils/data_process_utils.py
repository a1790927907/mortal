import json

from typing import List, Any
from pydantic import BaseModel, validate_model as _validate_model


# 将所有的"Object of type datetime is not JSON serializable" 直接转换掉
def format_dict_to_be_json_serializable(source: dict):
    def extract_list_data(source_list: list):
        for index, v in enumerate(source_list):
            if isinstance(v, dict):
                format_dict_to_be_json_serializable(v)
            elif isinstance(v, list):
                extract_list_data(v)
            else:
                try:
                    json.dumps(v)
                except TypeError as _e1:
                    source_list[index] = str(v)

    if source is None:
        return

    for key, value in source.items():
        if isinstance(value, list):
            extract_list_data(value)
        elif isinstance(value, dict):
            format_dict_to_be_json_serializable(value)
        else:
            if value is None:
                continue
            try:
                json.dumps(value)
            except TypeError as _e:
                source[key] = str(value)


def format_list_to_be_json_serializable(source: List[dict]):
    for s in source:
        format_dict_to_be_json_serializable(s)


def get_multiple_value_by_keys(keys: List[str], source: dict):
    result = [
        source.get(key) for key in keys
    ]
    return result


def validate_model(model: BaseModel):
    *_, error = _validate_model(model.__class__, model.dict())
    if error:
        raise error


def safe_load_json(source: str, *, return_when_error: Any = None):
    try:
        return json.loads(source)
    except Exception as _e:
        return return_when_error
