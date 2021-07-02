""" Task class module.
"""
import json
from datetime import datetime

from sqlalchemy import (JSON, Column, DateTime, Integer,  # type: ignore
                        MetaData, String, Table)

from .resultbase import ResultBase


class Task(ResultBase):
    """ Definition and storage of task ORM records.
    """

    def __init__(self, state: int, timestamp: datetime, repo_dir: str, task_type: int, params: str):
        """ Creates instances of task.

        Args:
            state (int): The task state.
            timestamp (datetime): Task creation timestamp.
            repo_dir (str): The task repository.
            task_type (int): The task type.
            params (str): The task parameters.
        """
        self.task_id: int
        self.state: int = state
        self.timestamp: datetime = timestamp
        self.repo_dir: str = repo_dir
        self.task_type: int = task_type
        self.params: str = params

    @staticmethod
    def _table_definition(metadata: MetaData) -> Table:
        """ Gets the definition of the tasks table.

        Args:
            metadata (MetaData): The database schema metadata.

        Returns:
            Table: Table following the tasks table definition.
        """
        return Table(
            "tasks",
            metadata,
            Column("task_id", Integer, primary_key=True),
            Column("state", Integer, nullable=False),
            Column("timestamp", DateTime, nullable=False),
            Column("repo_dir", String(128), nullable=False),
            Column("task_type", Integer, nullable=False),
            Column("params", JSON)
        )

    def __str__(self) -> str:
        return json.dumps({
            "task_id": self.task_id,
            "state": self.state,
            "timestamp": self.timestamp.strftime("%d-%m-%Y %H:%M:%S %Z"),
            "repo_dir": self.repo_dir,
            "task_type": self.task_type,
            "params": json.loads(self.params)
        })
