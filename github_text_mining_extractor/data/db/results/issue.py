""" Issue class module.
"""
import json
from typing import List
from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String, Boolean, JSON  # type: ignore
from .resultbase import ResultBase


class Issue(ResultBase):
    """ Definition and storage of issue ORM records.
    """

    def __init__(self, issue_id: int, repo_dir: str, title: str, description: str, labels: list, comments: dict, isPullRequest: bool):
        self.issue_id: int = issue_id
        self.repo_dir: str = repo_dir
        self.title: str = title
        self.description: str = description
        self.labels: List[str] = labels
        self.comments: List[str] = comments
        self.isPullRequest: bool = isPullRequest

    @staticmethod
    def _table_definition(metadata: MetaData) -> Table:
        return Table(
            "issues",
            metadata,
            Column("issue_id", String(128), primary_key=True),
            Column("repo_dir", Integer, ForeignKey(
                "repositories.repo_dir", ondelete="CASCADE"), primary_key=True),
            Column("title", String(60), nullable=False),
            Column("description", String, nullable=False),
            Column("labels", JSON),
            Column("comments", JSON),
            Column("isPullRequest", Boolean, nullable=False)
        )

    def __str__(self) -> str:
        return json.dumps({
            "issue_id": self.issue_id,
            "repo_dir": self.repo_dir,
            "title": self.title,
            "description": self.description,
            "labels": self.labels,
            "comments": self.comments,
            "isPullRequest": self.isPullRequest
        })
