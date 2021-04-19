""" Issue class module.
"""
import json
from typing import List

from sqlalchemy import (JSON, Boolean, Column, ForeignKey,  # type: ignore
                        Integer, MetaData, String, Table)

from .resultbase import ResultBase


class Issue(ResultBase):
    """ Definition and storage of issue ORM records.
    """

    def __init__(self, repo_dir: str, issue_id: int, title: str, description: str, labels: list, comments: list, isPullRequest: bool):
        """ Creates instances of issue.

        Args:
            repo_dir (str): The issue repository.
            issue_id (int): The issue identifier.
            title (str): The issue title.
            description (str): The issue description.
            labels (list): The issue labels.
            comments (dict): The issue comments.
            isPullRequest (bool): If true the issue is a pull request, otherwise false.
        """
        self.repo_dir: str = repo_dir
        self.issue_id: int = issue_id
        self.title: str = title
        self.description: str = description
        self.labels: List[str] = labels
        self.comments: List[str] = comments
        self.isPullRequest: bool = isPullRequest

    @staticmethod
    def _table_definition(metadata: MetaData) -> Table:
        """ Gets the definition of the issues table.

        Args:
            metadata (MetaData): The database schema metadata.

        Returns:
            Table: Table following the issues table definition.
        """
        return Table(
            "issues",
            metadata,
            Column("repo_dir", Integer, ForeignKey(
                "repositories.repo_dir", ondelete="CASCADE"), primary_key=True),
            Column("issue_id", String(128), primary_key=True),
            Column("title", String(60), nullable=False),
            Column("description", String, nullable=False),
            Column("labels", JSON),
            Column("comments", JSON),
            Column("isPullRequest", Boolean, nullable=False)
        )

    def __str__(self) -> str:
        return json.dumps({
            "repo_dir": self.repo_dir,
            "issue_id": self.issue_id,
            "title": self.title,
            "description": self.description,
            "labels": self.labels,
            "comments": self.comments,
            "isPullRequest": self.isPullRequest
        })
