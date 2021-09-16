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

""" Issue class module.
"""
import json

from sqlalchemy.dialects.mysql import LONGTEXT  # type: ignore
from sqlalchemy.sql.schema import (Column, ForeignKey,  # type: ignore
                                   MetaData, Table)
from sqlalchemy.sql.sqltypes import (JSON, Boolean, Integer,  # type: ignore
                                     String)

from .resultbase import ResultBase


class Issue(ResultBase):
    """ Definition and storage of issue ORM records.
    """

    def __init__(self,
                 repo_dir: str,
                 issue_id: int,
                 author: str,
                 title: str,
                 description: str,
                 labels: str,
                 is_pull_request: bool):
        """ Creates instances of issue.

        Args:
            repo_dir (str): The issue repository.
            issue_id (int): The issue identifier.
            author (str): The issue author.
            title (str): The issue title.
            description (str): The issue description.
            labels (list): The issue labels.
            is_pull_request (bool): If true the issue is a pull request, otherwise false.
        """
        self.repo_dir: str = repo_dir
        self.issue_id: int = issue_id
        self.author: str = author
        self.title: str = title
        self.description: str = description
        self.labels: str = labels
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
            Column("repo_dir", String(140),
                   ForeignKey("repositories.repo_dir", ondelete="CASCADE"),
                   primary_key=True),
            Column("issue_id", Integer, primary_key=True),
            Column("author", String(39), nullable=False),
            Column("title", String(255), nullable=False),
            Column("description", LONGTEXT, nullable=False),
            Column("labels", JSON),
            Column("is_pull_request", Boolean, nullable=False)
        )

    def __str__(self) -> str:
        return json.dumps({
            "repo_dir": self.repo_dir,
            "issue_id": self.issue_id,
            "author": self.author,
            "title": self.title,
            "description": self.description,
            "labels": json.loads(self.labels),
            "is_pull_request": self.is_pull_request
        })
