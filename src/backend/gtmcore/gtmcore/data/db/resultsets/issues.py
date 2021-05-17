""" Issues class module.
"""

import json
from typing import List, Optional

from gtmcore.data.db.err import IssueAlreadyExistsError, IssueNotExistsError
from gtmcore.data.db.results.issue import Issue  # type: ignore
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.query import Query  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore


class Issues():
    """ Class responsible of table-level issues operations for Issues.
    """
    @staticmethod
    def create(session: Session, repo_dir: str, issue_id: int, title: str, description: str,
               labels: list, comments: list, is_pull_request: bool) -> Issue:
        """ Creates a new Issue record.

        Args:
            session (Session): The database session.
            repo_dir (str): The issue repository.
            issue_id (int): The issue identifier.
            title (str): The issue title.
            description (str): The issue description.
            labels (list): The issue labels.
            comments (dict): The issue comments.
            is_pull_request (bool): If true the issue is a pull request, otherwise false.

        Raises:
            ValueError: Thrown when missing issue_id, repo_dir or title.
            IssueAlreadyExistError:
                Thrown when already exists an issuewith the same issue_id and repo_dir.

        Returns:
            Issue: The issue.
        """
        if not repo_dir or not issue_id or not title:
            raise ValueError(
                "You cannot create an issue without a repo_dir, an issue_id and a title.")
        try:
            labels_1: str = json.dumps(labels)
            comments_1: str = json.dumps(comments)
            issue: Issue = Issue(repo_dir, issue_id, title, description,
                                 labels_1, comments_1, is_pull_request)
            session.add(issue)
            session.commit()
            return issue
        except IntegrityError as err:
            raise IssueAlreadyExistsError() from err

    @staticmethod
    def get_issue(session: Session, repo_dir: str, issue_id: int) -> Issue:
        """ Gets an issue record from the repository.

        Args:
            session (Session): The database session.
            repo_dir (str): The issue repository.
            issue_id (int): The issue identifier.

        Raises:
            IssueNotExistsError:
                Thrown when there isn't any issue with that repo_dir and issue_id
                in the database records.

        Returns:
            Issue: The issue.
        """
        query: Query = session.query(Issue).filter_by(
            repo_dir=repo_dir, issue_id=issue_id)
        issue: Optional[Issue] = query.first()
        if issue is None:
            raise IssueNotExistsError()
        return issue

    @staticmethod
    def get_issues(session: Session, repo_dir: str = None, pull_requests=True) -> List[Issue]:
        """ Gets a list of issues.

        Args:
            session (Session): The database session.
            repo_dir (str, optional): The issue repository. Defaults to None.
            pull_requests (bool, optional): Filters the pull requests. Defaults to True.

        Returns:
            List[Issue]: List of issues.
        """
        query: Query = session.query(Issue)
        if repo_dir:
            query = query.filter_by(repo_dir=repo_dir)
        if not pull_requests:
            query = query.filter_by(is_pull_request=pull_requests)
        return query.all()
