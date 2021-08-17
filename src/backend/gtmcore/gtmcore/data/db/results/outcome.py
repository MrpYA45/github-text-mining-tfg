""" Outcome class module.
"""
import json

from sqlalchemy.sql.schema import (Column, ForeignKey,  # type: ignore
                                   MetaData, Table)
from sqlalchemy.sql.sqltypes import (JSON, Float, Integer,  # type: ignore
                                     String)

from .resultbase import ResultBase


class Outcome(ResultBase):
    """ Definition and storage of outcome ORM records.
    """

    def __init__(self,
                 task_id: int,
                 repo_dir: str,
                 model_type: str,
                 outcome_data: str,
                 exec_time: float):
        """Creates instances of outcome.

        Args:
            task_id (int): The task id.
            repo_dir (str): The task repository.
            model_type (str): The model type.
            outcome_data (str): The task outcome.
            exec_time (float): The task execution time.
        """
        self.task_id: int = task_id
        self.repo_dir: str = repo_dir
        self.model_type: str = model_type
        self.outcome_data: str = outcome_data
        self.exec_time: float = exec_time

    @staticmethod
    def _table_definition(metadata: MetaData) -> Table:
        """ Gets the definition of the outcome table.

        Args:
            metadata (MetaData): The database schema metadata.

        Returns:
            Table: Table following the issues table definition.
        """
        return Table(
            "outcomes",
            metadata,
            Column("task_id", Integer,
                   ForeignKey("tasks.task_id", ondelete="CASCADE"),
                   primary_key=True),
            Column("repo_dir", String(140),
                   ForeignKey("repositories.repo_dir", ondelete="CASCADE")),
            Column("model_type", String(10), nullable=False),
            Column("outcome_data", JSON, nullable=False),
            Column("exec_time", Float, nullable=False)
        )

    def __str__(self) -> str:
        return json.dumps({
            "task_id": self.task_id,
            "repo_dir": self.repo_dir,
            "model_type": self.model_type,
            "outcome_data": json.loads(self.outcome_data),
            "exec_time": self.exec_time
        })
