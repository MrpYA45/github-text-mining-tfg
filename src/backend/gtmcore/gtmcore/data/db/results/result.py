""" Result class module.
"""
import json

from sqlalchemy import (JSON, Column, ForeignKey, Integer,  # type: ignore
                        MetaData, Table)

from .resultbase import ResultBase


class Result(ResultBase):
    """ Definition and storage of result ORM records.
    """

    def __init__(self, task_id: int, task_type: int, result_data: str):
        """Creates instances of result.

        Args:
            task_id (int): [description]
            task_type (int): [description]
            result_data (str): [description]
        """
        self.task_id: int = task_id
        self.task_type: int = task_type
        self.result_data: str = result_data

    @staticmethod
    def _table_definition(metadata: MetaData) -> Table:
        """ Gets the definition of the result table.

        Args:
            metadata (MetaData): The database schema metadata.

        Returns:
            Table: Table following the issues table definition.
        """
        return Table(
            "results",
            metadata,
            Column("task_id", Integer, ForeignKey(
                "tasks.task_id", ondelete="CASCADE"), primary_key=True),
            Column("task_type", Integer, primary_key=True),
            Column("result_data", JSON, nullable=False),
        )

    def __str__(self) -> str:
        return json.dumps({
            "task_id": self.task_id,
            "task_type": self.task_type,
            "result_data": json.loads(self.result_data),
        })
