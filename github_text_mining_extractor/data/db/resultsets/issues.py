""" Issues class module.
"""

import json
from typing import List, Optional
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from ..results.issue import Issue


class Issues():
    """ Class responsible of table-level issues operations for Issues
    """
    @staticmethod
    def create(session: Session, issue_id: int, repo_dir: str, title: str, description: str, labels: list, comments: list, isPullRequest: bool) -> Issue:
        if not issue_id or not repo_dir or not title or not description:
            raise ValueError(
                "You cannot create a issue without an issue_id, an repo_dir, a title and a description.")
        try:
            issue = Issue(issue_id, repo_dir, title, description,
                          json.dumps(labels), json.dumps(comments), isPullRequest)
            session.add(issue)
            session.commit()
            return issue
        except IntegrityError:
            raise NotImplementedError

    @staticmethod
    def get_issue(session: Session, repo_dir: str, issue_id: int) -> Issue:
        query = session.query(Issue).filter_by(
            repo_dir=repo_dir, issue_id=issue_id)
        issue: Optional[Issue] = query.first()
        if issue is None:
            raise NotImplementedError
        return issue

    @staticmethod
    def get_issues(session: Session, repo_dir: str = None, pull_requests=True) -> List[Issue]:
        query = session.query(Issue)
        if str:
            query = query.filter_by(repo_dir=repo_dir)
        if not pull_requests:
            query = query.filter_by(isPullRequest=pull_requests)
        return query.all()
