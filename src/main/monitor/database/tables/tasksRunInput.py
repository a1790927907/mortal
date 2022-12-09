import sqlalchemy

from sqlalchemy.sql.functions import func
from src.main.monitor.config import Settings
from sqlalchemy.dialects.postgresql import JSONB


class Table(Settings.Base):
    __tablename__ = 'tasks_run_input'
    id = sqlalchemy.Column(sqlalchemy.String(600), primary_key=True)
    runId = sqlalchemy.Column(sqlalchemy.String(600), unique=True, nullable=False)
    input = sqlalchemy.Column(JSONB, nullable=False)
    createTime = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, server_default=func.now())
    updateTime = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, index=True)


table: sqlalchemy.Table = Table.__table__
table.metadata = Settings.metadata
