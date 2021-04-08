from datetime import datetime
from typing import List, Optional
from ..data.db import Schema, TaskTypes
from ..data.db.results import Task, Issue, Repository
from ..data.db.resultsets import Tasks, Issues, Repositories


class DBManager():

    def __init__(self, schema: Schema) -> None:
        self.__schema = schema

    def get_schema(self) -> Schema:
        return self.__schema.new_session()

    def create_task(self, timestamp: datetime, url: str) -> None:
        if not timestamp or not url:
            raise NotImplementedError
        session = self.get_schema()
        Tasks.create(session, TaskTypes.Queued.value, timestamp, url)

    def create_repository(self, repo_dir: str, title: str, description: str) -> None:
        if not repo_dir or not title or not description:
            raise NotImplementedError
        session = self.get_schema()
        Repositories.create(session, repo_dir, title, description)

    def create_issue(self, issue_id: int, repo_dir: str, title: str, description: str, labels: list, comments: list, isPullRequest: bool) -> None:
        if not issue_id or not repo_dir or not title or not description:
            raise NotImplementedError
        session = self.get_schema()
        Issues.create(session, issue_id, repo_dir, title, description,
                      labels, comments, isPullRequest)

    def get_task(self, task_id: int) -> Task:
        if not task_id:
            raise NotImplementedError
        session = self.get_schema()
        return Tasks.get_task(session, id)

    def get_tasks(self, state: str = None) -> List[Task]:
        session = self.get_schema()
        return Tasks.get_tasks(session, state)

    def get_repository(self, repo_dir: str) -> Repository:
        if not repo_dir:
            raise NotImplementedError
        session = self.get_schema()
        return Repositories.get_repository(session, repo_dir)

    def get_repositories(self) -> List[Repository]:
        session = self.get_schema()
        return Repositories.get_repositories(session)

    def get_issue(self, repo_dir: str, issue_id: int) -> Issue:
        if not repo_dir or not issue_id:
            raise NotImplementedError
        session = self.get_schema()
        return Issues.get_issue(session, repo_dir, issue_id)

    def get_issues(self, repo_dir: str = None, pull_requests=True) -> List[Issue]:
        session = self.get_schema()
        return Issues.get_issues(session, repo_dir, pull_requests)
