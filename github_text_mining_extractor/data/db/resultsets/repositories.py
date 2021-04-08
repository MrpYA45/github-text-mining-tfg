""" Repositories class module.
"""

from typing import List, Optional
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from ..results.repository import Repository


class Repositories():
    """ Class responsible of table-level repositories operations for Repositories
    """
    @staticmethod
    def create(session: Session, repo_dir: str, title: str, description: str) -> Repository:
        if not repo_dir or not title or not description:
            raise ValueError(
                "You cannot create a repository without an repo_dir, a title and a description.")
        try:
            repo = Repository(repo_dir, title, description)
            session.add(repo)
            session.commit()
            return repo
        except IntegrityError:
            raise NotImplementedError

    @staticmethod
    def get_repository(session: Session, repo_dir: str) -> Repository:
        query = session.query(Repository).filter_by(repo_dir=repo_dir)
        repo: Optional[Repository] = query.first()
        if repo is None:
            raise NotImplementedError
        return repo

    @staticmethod
    def get_repositories(session: Session) -> List[Repository]:
        query = session.query(Repository)
        return query.all()
