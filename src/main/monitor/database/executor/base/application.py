import databases

from typing import Type, Optional, List
from src.main.monitor.config import Settings
from src.main.monitor.base.application import Application as BaseApplication


class Application(BaseApplication):
    def __init__(self, settings: Type[Settings], db: databases.Database):
        super().__init__(settings)
        self.db = db

    async def get_db(self):
        if not self.db.is_connected:
            await self.db.connect()
        return self.db

    async def fetch_one(self, query) -> Optional[dict]:
        db = await self.get_db()
        result = await db.fetch_one(query)
        return dict(result) if result is not None else None

    async def fetch_all(self, query) -> List[dict]:
        db = await self.get_db()
        result: list = await db.fetch_all(query)
        return list(map(dict, result))
