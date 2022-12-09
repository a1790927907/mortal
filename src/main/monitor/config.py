import os
import sqlalchemy
import sqlalchemy_utils

from typing import Optional
from src.main.utils.logger import logger
from sqlalchemy.ext.declarative import declarative_base


def create_database(db_url: str):
    if not sqlalchemy_utils.database_exists(db_url):
        sqlalchemy_utils.create_database(db_url)
        logger.info("create database {} success".format(db_url))


def get_engine_and_metadata(db_url: str, *, schema: Optional[str] = None):
    create_database(db_url)
    engine = sqlalchemy.create_engine(db_url)
    if schema is None:
        metadata = sqlalchemy.MetaData()
    else:
        metadata = sqlalchemy.MetaData(schema=schema)
    metadata.bind = engine
    return engine, metadata


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
    db_url: str = "postgresql://{username}:{password}@{host}:{port}/{database}".format(
        username=db_user, password=db_password, host=db_host, port=db_port, database=db_database
    )
    engine, metadata = get_engine_and_metadata(db_url, schema=db_schema)
    Base = declarative_base(metadata=metadata, bind=engine)

    @classmethod
    def to_dict(cls):
        result = {}
        for key, value in cls.__annotations__.items():
            val = getattr(cls, key, None)
            if isinstance(val, str) or isinstance(val, int) or isinstance(val, float):
                result[key] = val
        return result

    @classmethod
    def create_all(cls):
        cls.Base.metadata.create_all()


tags_metadata = [
    {
        "name": "tasksRun",
        "description": "运行完毕的任务"
    },
    {
        "name": "taskStatus",
        "description": "运行完毕的任务状态"
    },
    {
        "name": "taskOutput",
        "description": "运行完毕的任务输出"
    },
    {
        "name": "tasksRunInput",
        "description": "运行完毕的任务的输入"
    },
    {
        "name": "tasksRunning",
        "description": "正在运行的任务"
    },
    {
        "name": "settings",
        "description": "配置信息"
    }
]
