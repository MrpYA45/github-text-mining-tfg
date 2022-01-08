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

""" Repository class module.
"""
import json

from sqlalchemy import Column, MetaData, String, Table, Text  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.sqltypes import JSON  # type: ignore

from .resultbase import ResultBase


class Repository(ResultBase):
    """ Definition and storage of repository ORM records.
    """

    def __init__(self, repo_dir: str, title: str, description: str, labels: str):
        """ Creates instances of repository.

        Args:
            repo_dir (str): The repository direction.
            title (str): The repository title.
            description (str): The repository description.
            labels (str): The repository labels.
        """
        self.repo_dir: str = repo_dir
        self.title: str = title
        self.description: str = description
        self.labels: str = labels

    @staticmethod
    def _table_definition(metadata: MetaData) -> Table:
        """ Gets the definition of the repositories table.

        Args:
            metadata (MetaData): The database schema metadata.

        Returns:
            Table: Table following the repositories table definition.
        """
        __table__ = Table(
            "repositories",
            metadata,
            Column("repo_dir", String(140), primary_key=True),
            Column("title", String(100), nullable=False),
            Column("description", Text, nullable=False),
            Column("labels", JSON)
        )
        issues = relationship(  # pylint: disable=unused-variable
            "Issue", foreign_keys=[__table__.c.repo_dir],
            backref="repository", passive_deletes=True)
        return __table__

    def __str__(self) -> str:
        return json.dumps({
            "repo_dir": self.repo_dir,
            "title": self.title,
            "description": self.description,
            "labels": json.loads(self.labels)
        })
