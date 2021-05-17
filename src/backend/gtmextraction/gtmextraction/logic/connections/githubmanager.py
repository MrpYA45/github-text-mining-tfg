import time
from datetime import datetime, timedelta
from typing import List, Tuple
from urllib.parse import urlparse

from github import RateLimitExceededException
from github.GithubException import BadCredentialsException
from gtmcore.logic.dbmanager import DBManager

from .githubconnection import GitHubConnection


class GitHubManager():

    def __init__(self, gh_conn: GitHubConnection, manager: DBManager) -> None:
        self.gh_conn = gh_conn
        self.manager = manager

    def get_repo_info(self, repo_dir: str) -> Tuple:
        try:
            session = self.gh_conn.get_session()
            repo = session.get_repo(repo_dir)
            return (repo.full_name, repo.description)
        except BadCredentialsException as err:
            raise ValueError("Invalid GitHub Access Token.") from err

    def get_repo_issues(self, repo_dir: str) -> List[dict]:
        session = self.gh_conn.get_session()
        repo = session.get_repo(repo_dir)
        issues = repo.get_issues(state="all")
        iter_issues = iter(issues)
        issues_data = []
        while True:
            try:
                issue = next(iter_issues)
                labels = self.__get_labels_from_issue(issue)
                comments = self.__get_comments_from_issue(issue)
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

    def __get_labels_from_issue(self, issue) -> List[str]:
        labels = []
        iter_labels = iter(issue.labels)
        while True:
            try:
                label = next(iter_labels)
                labels.append(label.name)
            except StopIteration:
                return labels
            except RateLimitExceededException:
                sleep_time = (self.gh_conn.get_rate_limit_reset() - datetime.utcnow() +
                              timedelta(0, 20)).total_seconds()
                time.sleep(sleep_time)

    def __get_comments_from_issue(self, issue) -> List[str]:
        comments = []
        iter_labels = iter(issue.get_comments())
        while True:
            try:
                comment = next(iter_labels)
                comments.append(comment.body)
            except StopIteration:
                return comments
            except RateLimitExceededException:
                sleep_time = (self.gh_conn.get_rate_limit_reset() - datetime.utcnow() +
                              timedelta(0, 20)).total_seconds()
                time.sleep(sleep_time)

    @staticmethod
    def get_repo_dir(url: str):
        return urlparse(url).path[1:]
