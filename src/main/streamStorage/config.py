import os
import databases
import sqlalchemy

from typing import Optional
from src.main.utils.logger import logger
from sqlalchemy_utils import create_database, database_exists


def get_engine(url: str):
    return sqlalchemy.create_engine(url)


def get_metadata(engine: sqlalchemy.engine.Engine, *, schema: Optional[str] = None):
    if schema is not None:
        metadata = sqlalchemy.MetaData(schema=schema)
    else:
        metadata = sqlalchemy.MetaData()
    metadata.bind = engine
    return metadata


def get_engine_and_metadata(url: str, *, schema: Optional[str] = None):
    if not database_exists(url):
        create_database(url)
        logger.info("创建 {} 成功".format(url))
    engine = get_engine(url)
    return engine, get_metadata(engine, schema=schema)


tags_metadata = [
    {
        "name": "connection",
        "description": "流执行连接相关"
    },
    {
        "name": "task",
        "description": "流任务相关"
    },
    {
        "name": "schema",
        "description": "schema相关(主要用于触发时的input)"
    },
    {
        "name": "settings",
        "description": "配置相关"
    }
]


class Settings:
    author: str = "zyh"
    description: str = "看你ma看"
    version: str = "1.0.0"
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_user: str = os.getenv("DB_USER", "postgres")
    db_password: str = os.getenv("DB_PASSWORD", "postgres")
    db_port: int = int(os.getenv("DB_PORT", "5433"))
    db_database: str = os.getenv("DB_DATABASE", "stream")
    db_schema: Optional[str] = os.getenv("DB_SCHEMA")
    # postgresql://postgres:postgres@localhost:5433/novel
    db_url: str = "postgresql://{username}:{password}@{host}:{port}/{database}".format(
        username=db_user, password=db_password, host=db_host, port=db_port, database=db_database
    )
    engine, metadata = get_engine_and_metadata(db_url, schema=db_schema)
    db_instance: databases.Database = databases.Database(db_url)

    @classmethod
    def to_dict(cls):
        result = {}
        for key, value in cls.__annotations__.items():
            val = getattr(cls, key, None)
            if isinstance(val, str) or isinstance(val, int) or isinstance(val, float):
                result[key] = val
        return result
