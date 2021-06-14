import logging
import time
from datetime import datetime, timedelta
from typing import Callable, Iterator, List, Optional, Tuple
from urllib.parse import urlparse

from github import RateLimitExceededException
from github.GithubException import BadCredentialsException
from github.Repository import Repository
from gtmcore.data.db.results.task import Task
from gtmcore.logic.dbmanager import DBManager
from sqlalchemy.orm.session import Session  # type: ignore

from .githubconnection import GitHubConnection


class GitHubManager():

    def __init__(self, gh_conn: GitHubConnection, manager: DBManager) -> None:
        self.gh_conn = gh_conn
        self.manager = manager

    def get_repo_info(self, repo_dir: str) -> Tuple:
        try:
            session: Session = self.gh_conn.get_session()
            repo: Repository = session.get_repo(repo_dir)
            labels: List[str] = self.__get_basic_iterable_data(
                iter(repo.get_labels()), "name")
            return (repo.full_name, repo.description, labels)
        except BadCredentialsException as err:
            raise ValueError("Invalid GitHub Access Token.") from err

    def get_repo_issues(self, task: Task, is_outdated: Callable) -> Optional[List[dict]]:
        session = self.gh_conn.get_session()
        repo = session.get_repo(task.repo_dir)
        issues = repo.get_issues(state="all")
        iter_issues = iter(issues)
        issues_data = []
        while True:
            if is_outdated(task):
                logging.debug(
                    "[GTMExtraction] ABORTING DATA EXTRACTION FROM REPO: %s. REASON: Outdated Task",
                    task.repo_dir)
                return None
            try:
                issue = next(iter_issues)
                labels = self.__get_basic_iterable_data(
                    iter(issue.labels), "name")
                comments = self.__get_basic_iterable_data(
                    iter(issue.get_comments()), "body")
                is_pull_request = issue.pull_request is not None
                issue_data = {
                    "id": issue.id,
                    "title": issue.title,
                    "description": issue.body,
                    "labels": labels,
                    "comments": comments,
                    "is_pull_request": is_pull_request
                }
                issues_data.append(issue_data)
            except StopIteration:
                return issues_data
            except RateLimitExceededException:
                sleep_time = (self.gh_conn.get_rate_limit_reset() - datetime.utcnow() +
                              timedelta(0, 20)).total_seconds()
                time.sleep(sleep_time)

    def __get_basic_iterable_data(self, it: Iterator, property_name: str) -> List[str]:
        data = []
        while True:
            try:
                item = next(it)
                data.append(getattr(item, property_name))
            except StopIteration:
                return data
            except RateLimitExceededException:
                sleep_time = (self.gh_conn.get_rate_limit_reset() - datetime.utcnow() +
                              timedelta(0, 20)).total_seconds()
                time.sleep(sleep_time)

    @ staticmethod
    def get_repo_dir(url: str):
        return urlparse(url).path[1:]
