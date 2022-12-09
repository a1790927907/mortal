import sqlalchemy

from sqlalchemy.sql.functions import func
from src.main.monitor.config import Settings
from sqlalchemy.dialects.postgresql import JSONB


class Table(Settings.Base):
    __tablename__ = 'task_output'
    id = sqlalchemy.Column(sqlalchemy.String(600), primary_key=True)
    taskStatusId = sqlalchemy.Column(sqlalchemy.String(600), index=True, nullable=False)
    taskId = sqlalchemy.Column(sqlalchemy.String(600), index=True, nullable=False)
    output = sqlalchemy.Column(JSONB, nullable=True)
    createTime = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, server_default=func.now())
    updateTime = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, index=True)


table: sqlalchemy.Table = Table.__table__
table.metadata = Settings.metadata
