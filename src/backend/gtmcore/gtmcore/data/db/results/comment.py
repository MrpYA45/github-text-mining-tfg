# Copyright (C) 2021 Pablo Fernández Bravo
#
# This file is part of github-text-mining-tfg.
#
# github-text-mining-tfg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# github-text-mining-tfg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with github-text-mining-tfg.  If not, see <http://www.gnu.org/licenses/>.

""" Comment class module.
"""
import json

from sqlalchemy.sql.schema import (Column,  # type: ignore
                                   ForeignKeyConstraint, MetaData, Table)
from sqlalchemy.sql.sqltypes import Integer, String, Text  # type: ignore

from .resultbase import ResultBase


class Comment(ResultBase):
    """ Definition and storage of comment ORM records.
    """

    def __init__(self, repo_dir: str,
                 issue_id: int,
                 comment_id: int,
                 author: str,
                 body: str):
        """ Creates instances of comment.

        Args:
            repo_dir (str): The issue repository.
            issue_id (int): The issue identifier.
            comment_id (int): The comment identifier.
            author (str): The comment author.
            body (str): The comment body.
        """
        self.repo_dir: str = repo_dir
        self.issue_id: int = issue_id
        self.comment_id: int = comment_id
        self.author: str = author
        self.body: str = body

    @staticmethod
    def _table_definition(metadata: MetaData) -> Table:
        """ Gets the definition of the comments table.

        Args:
            metadata (MetaData): The database schema metadata.

        Returns:
            Table: Table following the comments table definition.
        """
        return Table(
            "comments",
            metadata,
            Column("repo_dir", String(140), primary_key=True),
            Column("issue_id", Integer, primary_key=True),
            Column("comment_id", Integer, primary_key=True),
            Column("author", String(39), nullable=False),
            Column("body", Text, nullable=False),
            ForeignKeyConstraint(["repo_dir", "issue_id"],
                                 ["issues.repo_dir", "issues.issue_id"],
                                 ondelete="CASCADE")
        )

    def __str__(self) -> str:
        return json.dumps({
            "repo_dir": self.repo_dir,
            "issue_id": self.issue_id,
            "comment_id": self.comment_id,
            "author": self.author,
            "body": self.body
        })
