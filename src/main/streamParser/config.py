import os


tags_metadata = [
    {
        "name": "n8nParser",
        "description": "n8n流解析"
    },
    {
        "name": "settings",
        "description": "配置相关"
    }
]


class Settings:
    author: str = "zyh"
    version: str = "1.0.0"
    description: str = "sb"
    function_codes_dir: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/functionCodes")

    @classmethod
    def to_dict(cls):
        result = {}
        for key, value in cls.__annotations__.items():
            val = getattr(cls, key, None)
            if isinstance(val, str) or isinstance(val, int) or isinstance(val, float):
                result[key] = val
        return result
