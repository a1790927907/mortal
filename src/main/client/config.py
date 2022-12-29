import os

from src.main.globalSettings.config import Settings as globalSettings


class Settings:
    redis_server: str = os.getenv("REDIS_SERVER", "redis://localhost:6379")
    json_schema_model_cache_key: str = os.getenv("JSON_SCHEMA_CACHE_KEY", "json_schema_model_path")
    tasks_running_mapping_key: str = os.getenv("TASKS_RUNNING_MAPPING_KEY", "tasks_running_mapping")
    model_cache_dir: str = globalSettings.model_cache_dir
