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

""" GitHub Manager class module.
"""

import logging
import time
from datetime import datetime, timedelta
from typing import Callable, Iterator

from github import RateLimitExceededException
from github.GistComment import GistComment
from github.GithubException import BadCredentialsException
from github.Issue import Issue
from github.MainClass import Github
from github.Repository import Repository
from gtmcore.data.db.results.task import Task
from gtmcore.logic.dbmanager import DBManager
from gtmcore.logic.utils.datautils import DataUtils
from sqlalchemy.orm.session import Session  # type: ignore

from .githubconnection import GitHubConnection


class GitHubManager():
    """ Class in charge of gathering the data from GitHub.
    """

    def __init__(self, gh_conn: GitHubConnection, db_manager: DBManager) -> None:
        self.__gh_conn = gh_conn
        self.__db_manager = db_manager

    def get_repo_info(self, repo_dir: str) -> bool:
        """ Gets the repository information.

        Args:
            repo_dir (str): The repository direction.

        Raises:
            ValueError: Thrown when the GitHub Session is not valid.

        Returns:
            Tuple: The repository name, description and labels.
        """
        try:
            session: Session = self.__gh_conn.get_session()
            repo: Repository = session.get_repo(repo_dir)
            self.__db_manager.create_repository(
                repo_dir,
                repo.name,
                self.__downloaded_data_cleaner(repo.description or ""),
                self.__get_basic_iterable_data(iter(repo.get_labels()), "name")
            )
            return True
        except BadCredentialsException as err:
            logging.exception("[GTMExtraction] INVALID GITHUB ACCESS TOKEN.")
            raise err

    def get_repo_issues(self, task: Task, is_outdated: Callable) -> bool:
        """ Gets the issues information.

        Args:
            task (Task): The task that requires the issues data.
            is_outdated (Callable): A function which checks
                if the task gets outdated during the download process.

        Returns:
            Optional[List[dict]]: List of dictionaries,
                each one with the data associated with an issue.
        """
        session: Github = self.__gh_conn.get_session()
        repo: Repository = session.get_repo(task.repo_dir)
        issues = repo.get_issues(state="all")
        iter_issues: Iterator = iter(issues)

        while True:
            if is_outdated(task):
                logging.debug(
                    "[GTMExtraction] ABORTING DATA EXTRACTION FROM REPO: %s. REASON: Outdated Task",
                    task.repo_dir)
                return False

            try:
                issue: Issue = next(iter_issues)
                self.__db_manager.create_issue(
                    task.repo_dir,
                    issue.id,
                    issue.user.login,
                    self.__downloaded_data_cleaner(issue.title or ""),
                    self.__downloaded_data_cleaner(issue.body or ""),
                    self.__get_basic_iterable_data(iter(issue.labels), "name"),
                    issue.pull_request is not None
                )

                self.get_issue_comments(task, issue)

            except StopIteration:
                return True

            except RateLimitExceededException:
                sleep_time: float = (self.__gh_conn.get_rate_limit_reset() - datetime.utcnow() +
                                     timedelta(0, 20)).total_seconds()
                time.sleep(sleep_time)
                continue

    def get_issue_comments(self, task: Task, issue: Issue) -> bool:
        """ Gets the issues information.

        Args:
            task (Task): The task that requires the issues data.
            is_outdated (Callable): A function which checks
                if the task gets outdated during the download process.

        Returns:
            Optional[List[dict]]: List of dictionaries,
                each one with the data associated with a comment.
        """
        comments = issue.get_comments()
        iter_comments: Iterator = iter(comments)

        while True:
            try:
                comment: GistComment = next(iter_comments)
                self.__db_manager.create_comment(
                    task.repo_dir,
                    issue.id,
                    comment.id,
                    comment.user.login,
                    self.__downloaded_data_cleaner(comment.body or "")
                )

            except StopIteration:
                return True

            except RateLimitExceededException:
                sleep_time: float = (self.__gh_conn.get_rate_limit_reset() - datetime.utcnow() +
                                     timedelta(0, 20)).total_seconds()
                time.sleep(sleep_time)
                continue

    def __get_basic_iterable_data(self, iterator: Iterator, property_name: str) -> list:
        """ Extract the value of a property inside each of the objects of an iterator into a list.

        Args:
            iterator (Iterator): The iterator.
            property_name (str): The exact name of the object property.

        Returns:
            list: A list containing the property value of each object.
        """
        data: list = []
        while True:
            try:
                item = next(iterator)
                markdown_data = getattr(item, property_name)
                data.append(self.__downloaded_data_cleaner(markdown_data or ""))
            except StopIteration:
                return data
            except RateLimitExceededException:
                sleep_time: float = (self.__gh_conn.get_rate_limit_reset() - datetime.utcnow() +
                                     timedelta(0, 20)).total_seconds()
                time.sleep(sleep_time)

    def __downloaded_data_cleaner(self, md_str: str) -> str:
        """ Clears all markdown and non ASCII characters from the given raw string.

        Args:
            md_str (str): String with markdown, emojis and other non ASCII characters.

        Returns:
            str: A string without markdown or non ASCII characters.
        """
        raw_text = DataUtils.markdown_to_raw_text(md_str)
        return DataUtils.remove_non_ascii_chars(raw_text)
