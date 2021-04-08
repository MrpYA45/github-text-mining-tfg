import time
from urllib.parse import urlparse
from github import Issue, RateLimitExceededException
from typing import List
from datetime import datetime

from ..dbmanager import DBManager
from ...data.db.schema import Schema
from .githubconection import GitHubConnection
from ...data.db import schema


class GitHubManager():

    def __init__(self, gh_conn: GitHubConnection, manager: DBManager) -> None:
        self.session = gh_conn.get_session()
        self.manager = manager

    def get_repo_dir(self, url: str):
        return urlparse(url).path[1:]

    def add_repo_info_into_db(self, repo_dir: str) -> None:
        repo = self.session.get_repo(repo_dir)
        self.manager.create_repository(
            repo_dir, repo.full_name, repo.description)

    def add_issues_info_into_db(self, repo_dir: str) -> None:
        repo = self.session.get_repo(repo_dir)
        issues = repo.get_issues(state="all")
        iter_issues = iter(issues)
        while True:
            try:
                issue = next(iter_issues)
                labels = self.get_labels_from_issue(issue)
                comments = self.get_comments_from_issue(issue)
                isPullRequest = issue.pull_request is not None
                self.manager.create_issue(
                    issue.id, repo_dir, issue.title, issue.body, labels, comments, isPullRequest)
            except StopIteration:
                return
            except RateLimitExceededException:
                sleep_time = self.session.get_rate_limit_reset() - datetime.utcnow() + \
                    datetime.timedelta(0, 20)
                time.sleep(sleep_time)

    def get_labels_from_issue(self, issue: Issue) -> List[str]:
        labels = []
        iter_labels = iter(issue.labels)
        while True:
            try:
                label = next(iter_labels)
                labels.append(label.name)
            except StopIteration:
                return labels
            except RateLimitExceededException:
                sleep_time = self.session.get_rate_limit_reset() - datetime.utcnow() + \
                    datetime.timedelta(0, 20)
                time.sleep(sleep_time)

    def get_comments_from_issue(self, issue: Issue) -> List[str]:
        comments = []
        iter_labels = iter(issue.get_comments())
        while True:
            try:
                comment = next(iter_labels)
                comments.append(comment.body)
            except StopIteration:
                return comments
            except RateLimitExceededException:
                sleep_time = self.session.get_rate_limit_reset() - datetime.utcnow() + \
                    datetime.timedelta(0, 20)
                time.sleep(sleep_time)
