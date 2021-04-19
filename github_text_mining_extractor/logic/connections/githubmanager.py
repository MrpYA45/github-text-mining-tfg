import time
from datetime import datetime
from typing import List, Tuple
from urllib.parse import urlparse

from data.db import DBManager
from github import Issue, RateLimitExceededException
from github.GithubException import BadCredentialsException

from .githubconnection import GitHubConnection


class GitHubManager():

    def __init__(self, gh_conn: GitHubConnection, manager: DBManager) -> None:
        self.session = gh_conn.get_session()
        self.manager = manager

    def get_repo_info(self, repo_dir: str) -> Tuple:
        try:
            repo = self.session.get_repo(repo_dir)
            return (repo.full_name, repo.description)
        except BadCredentialsException:
            raise ValueError("Invalid GitHub Access Token.")

    def get_repo_issues(self, repo_dir: str) -> List[dict]:
        repo = self.session.get_repo(repo_dir)
        issues = repo.get_issues(state="all")
        iter_issues = iter(issues)
        issues_data = []
        while True:
            try:
                issue = next(iter_issues)
                labels = self.__get_labels_from_issue(issue)
                comments = self.__get_comments_from_issue(issue)
                isPullRequest = issue.pull_request is not None
                issue_data = {
                    "id": issue.id,
                    "title": issue.title, 
                    "description": issue.body,
                    "labels": labels, 
                    "comments": comments, 
                    "isPullRequest": isPullRequest
                    }
                issues_data.append(issue_data)
            except StopIteration:
                return issues_data
            except RateLimitExceededException:
                sleep_time = self.session.get_rate_limit_reset() - datetime.utcnow() + \
                    datetime.timedelta(0, 20)
                time.sleep(sleep_time)

    def __get_labels_from_issue(self, issue: Issue) -> List[str]:
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

    def __get_comments_from_issue(self, issue: Issue) -> List[str]:
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

    @staticmethod
    def get_repo_dir(url: str):
        return urlparse(url).path[1:]
