import sqlalchemy
from sqlalchemy.engine import Engine
from typing import Any, List, Optional
from src.main.streamStorage.config import Settings
from sqlalchemy.ext.declarative import declarative_base
from src.main.streamStorage.base.application import Application as BaseApplication


def get_base(engine: Engine, metadata: sqlalchemy.MetaData):
    return declarative_base(metadata=metadata, bind=engine)


Base = get_base(Settings.engine, Settings.metadata)


class Application(BaseApplication):
    async def get_db(self):
        if not self.settings.db_instance.is_connected:
            await self.settings.db_instance.connect()
        return self.settings.db_instance

    async def fetch_all(self, query: Any) -> List[dict]:
        db = await self.get_db()
        result: list = await db.fetch_all(query)
        return list(map(dict, result))

    async def fetch_one(self, query: Any) -> Optional[dict]:
        db = await self.get_db()
        result = await db.fetch_one(query)
        return dict(result) if result is not None else None
