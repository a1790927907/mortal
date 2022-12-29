import sqlalchemy

from sqlalchemy.sql.functions import func
from src.main.monitor.config import Settings


class Table(Settings.Base):
    __tablename__ = 'tasks_run'
    id = sqlalchemy.Column(sqlalchemy.String(600), primary_key=True)
    executeTime = sqlalchemy.Column(sqlalchemy.Float, nullable=True, index=True)
    status = sqlalchemy.Column(sqlalchemy.String(600), nullable=False, index=True)
    connectionId = sqlalchemy.Column(sqlalchemy.String(600), nullable=False, index=True)
    openid = sqlalchemy.Column(sqlalchemy.String(600), nullable=False, index=True)
    startTime = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, index=True)
    endTime = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, index=True)
    createTime = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, server_default=func.now())
    updateTime = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, index=True)


table: sqlalchemy.Table = Table.__table__
table.metadata = Settings.metadata
