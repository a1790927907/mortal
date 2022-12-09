import os


class Settings:
    redis_server: str = os.getenv("REDIS_SERVER", "redis://localhost:6379")
    json_schema_model_cache_key: str = os.getenv("JSON_SCHEMA_CACHE_KEY", "json_schema_model_path")
    model_cache_dir: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/pyModel")
