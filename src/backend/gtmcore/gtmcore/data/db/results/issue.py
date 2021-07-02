""" Issue class module.
"""
import json

from sqlalchemy import (JSON, Boolean, Column, ForeignKey,  # type: ignore
                        Integer, MetaData, String, Table, Text)

from .resultbase import ResultBase


class Issue(ResultBase):
    """ Definition and storage of issue ORM records.
    """

    def __init__(self, repo_dir: str, issue_id: int, title: str, description: str, labels: str,
                 comments: str, is_pull_request: bool):
        """ Creates instances of issue.

        Args:
            repo_dir (str): The issue repository.
            issue_id (int): The issue identifier.
            title (str): The issue title.
            description (str): The issue description.
            labels (list): The issue labels.
            comments (dict): The issue comments.
            is_pull_request (bool): If true the issue is a pull request, otherwise false.
        """
        self.repo_dir: str = repo_dir
        self.issue_id: int = issue_id
        self.title: str = title
        self.description: str = description
        self.labels: str = labels
        self.comments: str = comments
        self.is_pull_request: bool = is_pull_request

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
            Column("repo_dir", String(140), ForeignKey(
                "repositories.repo_dir", ondelete="CASCADE"), primary_key=True),
            Column("issue_id", Integer, primary_key=True),
            Column("title", String(255), nullable=False),
            Column("description", Text, nullable=False),
            Column("labels", JSON),
            Column("comments", JSON),
            Column("is_pull_request", Boolean, nullable=False)
        )

    def __str__(self) -> str:
        return json.dumps({
            "repo_dir": self.repo_dir,
            "issue_id": self.issue_id,
            "title": self.title,
            "description": self.description,
            "labels": json.loads(self.labels),
            "comments": json.loads(self.comments),
            "is_pull_request": self.is_pull_request
        })
