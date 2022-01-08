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

""" Repositories class module.
"""

import json
from typing import List, Optional

from gtmcore.data.db.err import (RepositoryAlreadyExistError,
                                 RepositoryNotExistsError)
from gtmcore.data.db.results.repository import Repository
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.query import Query  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore


class Repositories():
    """ Class responsible of table-level repositories operations for Repositories.
    """
    @staticmethod
    def create(session: Session, repo_dir: str, title: str,
               description: str, labels: list) -> Repository:
        """ Creates a new Repository record.

        Args:
            session (Session): The database session.
            repo_dir (str): The repository direction.
            title (str): The repository title.
            description (str): The repository description.
            labels (str): The repository labels.

        Raises:
            ValueError: Thrown when missing repo_dir or title.
            RepositoryAlreadyExistError:
                Thrown when already exists a repository with the same repo_dir.

        Returns:
            Repository: The repository.
        """
        if not repo_dir or not title:
            raise ValueError(
                "You cannot create a repository without a repo_dir and a title.")
        try:
            labels_1: str = json.dumps(labels)
            repo: Repository = Repository(
                repo_dir, title, description, labels_1)
            session.add(repo)
            session.commit()
            return repo
        except IntegrityError as err:
            session.rollback()
            raise RepositoryAlreadyExistError from err

    @staticmethod
    def delete(session: Session, repo_dir: str) -> None:
        """ Deletes the specified Repository record.

        Args:
            session (Session): The database session.
            repo_dir (str): The repository direction.

        Raises:
            ValueError: Thrown when missing repo_dir.
        """
        if not repo_dir:
            raise ValueError(
                "You cannot create a repository without a repo_dir.")
        session.query(Repository).filter_by(repo_dir=repo_dir).delete()
        session.commit()

    @staticmethod
    def get_repository(session: Session, repo_dir: str) -> Repository:
        """ Gets the repository record.

        Args:
            session (Session): The database session.
            repo_dir (str): The repository direction.

        Raises:
            RepositoryNotExistsError:
                Thrown when there isn't any repository with that repo_dir in the database records.

        Returns:
            Repository: The repository.
        """
        query: Query = session.query(Repository).filter_by(repo_dir=repo_dir)
        repo: Optional[Repository] = query.first()
        if repo is None:
            raise RepositoryNotExistsError
        return repo

    @staticmethod
    def get_repositories(session: Session) -> List[Repository]:
        """Gets all the repositories.

        Args:
            session (Session): The database session.

        Returns:
            List[Repository]: List with all the repositories.
        """
        query: Query = session.query(Repository)
        return query.all()
