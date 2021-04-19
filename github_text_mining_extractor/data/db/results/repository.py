""" Repository class module.
"""
import json
from datetime import datetime

from sqlalchemy import (JSON, Column, ForeignKey, Integer,  # type: ignore
                        MetaData, String, Table)

from .resultbase import ResultBase


class Repository(ResultBase):
    """ Definition and storage of repository ORM records.
    """

    def __init__(self, repo_dir: str, title: str, description: str):
        """ Creates instances of repository.

        Args:
            repo_dir (str): The repository direction.
            title (str): The repository title.
            description (str): The repository description.
        """
        self.repo_dir: str = repo_dir
        self.title: str = title
        self.description: str = description

    @staticmethod
    def _table_definition(metadata: MetaData) -> Table:
        """ Gets the definition of the repositories table.

        Args:
            metadata (MetaData): The database schema metadata.

        Returns:
            Table: Table following the repositories table definition.
        """
        return Table(
            "repositories",
            metadata,
            Column("repo_dir", String(128), primary_key=True),
            Column("title", String(60), nullable=False),
            Column("description", String, nullable=False)
        )

    def __str__(self) -> str:
        return json.dumps({
            "repo_dir": self.repo_dir,
            "title": self.title,
            "description": self.description
        })
