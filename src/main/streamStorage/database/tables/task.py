import sqlalchemy
from sqlalchemy.sql.functions import func
from sqlalchemy.dialects.postgresql import JSONB
from src.main.streamStorage.config import Settings
from src.main.streamStorage.database.base.application import Base


class Table(Base):
    __tablename__ = 'task'
    id = sqlalchemy.Column(sqlalchemy.String(600), primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(600), index=True, nullable=False)
    type = sqlalchemy.Column(sqlalchemy.String(600), index=True, nullable=False)
    connectionId = sqlalchemy.Column(sqlalchemy.String(600), index=True, nullable=False)
    payload = sqlalchemy.Column(JSONB, nullable=False)
    createTime = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, server_default=func.now())
    updateTime = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, index=True)


table: sqlalchemy.Table = Table.__table__
table.metadata = Settings.metadata
