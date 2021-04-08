""" Task class module.
"""
import json
from datetime import datetime
from .resultbase import ResultBase
from sqlalchemy import Table, MetaData, Column, ForeignKey, Sequence, Integer, String, DateTime  # type: ignore
from .resultbase import ResultBase


class Task(ResultBase):
    """ Definition and storage of task ORM records.
    """

    def __init__(self, state: int, timestamp: datetime, url: str):
        self.state: int = state
        self.timestamp: datetime = timestamp
        self.url: str = url

    @staticmethod
    def _table_definition(metadata: MetaData) -> Table:
        return Table(
            "tasks",
            metadata,
            Column("task_id", Integer, primary_key=True),
            Column("state", Integer, nullable=False),
            Column("timestamp", DateTime, nullable=False),
            Column("url", String(128), nullable=False)
        )

    def __str__(self) -> str:
        return json.dumps({
            "task_id": self.task_id,
            "state": self.state,
            "timestamp": self.timestamp.strftime("%d-%m-%Y %H:%M:%S %Z"),
            "url": self.url
        })
