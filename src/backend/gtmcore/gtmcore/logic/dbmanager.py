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


""" Database Manager Class Module.
"""

from datetime import datetime
from typing import List

from gtmcore.data.db import Schema
from gtmcore.data.db.enums import TaskState, TaskType
from gtmcore.data.db.err.repositoryalreadyexistserror import \
    RepositoryAlreadyExistError
from gtmcore.data.db.results import Issue, Repository, Task
from gtmcore.data.db.results.comment import Comment
from gtmcore.data.db.results.outcome import Outcome
from gtmcore.data.db.resultsets import Issues, Repositories, Tasks
from gtmcore.data.db.resultsets.comments import Comments
from gtmcore.data.db.resultsets.outcomes import Outcomes


class DBManager():
    """ Class responsible of table-level database operations.
    """

    def __init__(self, schema: Schema) -> None:
        self.__schema = schema

    def get_schema(self) -> Schema:
        """ Gets the database schema.

        Returns:
            Schema: The database schema.
        """
        return self.__schema.new_session()

    def create_repository(self,
                          repo_dir: str,
                          title: str,
                          description: str,
                          labels: list) -> Repository:
        """ Creates a new Repository record.

        Args:
            repo_dir (str): The repository direction.
            title (str): The repository title
            description (str): The repository description.
            labels (list): The repository labels.

        Raises:
            ValueError: Thrown when missing repo_dir or title.

        Returns:
            Repository: The repository.
        """
        if not repo_dir or not title:
            raise ValueError(
                "You cannot create a repository without a repo_dir and a title.")
        session: Schema = self.get_schema()
        try:
            repo: Repository = Repositories.create(
                session, repo_dir, title, description, labels)
        except RepositoryAlreadyExistError:
            Repositories.delete(session, repo_dir)
            repo = Repositories.create(
                session, repo_dir, title, description, labels)
        return repo

    def delete_repository(self, repo_dir: str) -> None:
        """ Deletes the specified Repository record.

        Args:
            repo_dir (str): The repository direction.

        Raises:
            ValueError: Thrown when missing repo_dir.
        """
        if not repo_dir:
            raise ValueError(
                "You cannot delete a repository without a repo_dir.")
        session: Schema = self.get_schema()
        Repositories.delete(session, repo_dir)

    def get_repository(self, repo_dir: str) -> Repository:
        """ Gets the specified repository record.

        Args:
            session (Session): The database session.
            repo_dir (str): The repository direction.

        Raises:
            ValueError: Thrown when missing repo_dir.

        Returns:
            Repository: The repository.
        """
        if not repo_dir:
            raise ValueError("You cannot get a repository without a repo_dir.")
        session: Schema = self.get_schema()
        return Repositories.get_repository(session, repo_dir)

    def get_repositories(self) -> List[Repository]:
        """Gets all the repositories.

        Returns:
            List[Repository]: List with all the repositories.
        """
        session: Schema = self.get_schema()
        return Repositories.get_repositories(session)

    def create_issue(self,
                     repo_dir: str,
                     issue_id: int,
                     author: str,
                     title: str,
                     description: str,
                     labels: list,
                     is_pull_request: bool) -> Issue:
        """ Creates a new issue.

        Args:
            repo_dir (str): The issue repository.
            issue_id (int): The issue identifier.
            author (str): The issue author.
            title (str): The issue title.
            description (str): The issue description.
            labels (list): The issue labels.
            is_pull_request (bool): If true the issue is a pull request, otherwise false.

        Raises:
            ValueError: Thrown when missing repo_dir, issue_id, author or title.

        Returns:
            Issue: The issue.
        """
        if not repo_dir or issue_id is None or not author or not title:
            raise ValueError(
                "You cannot create an issue without a repo_dir, "
                "an issue_id, an author and a title.")
        session: Schema = self.get_schema()
        return Issues.create(
            session, repo_dir, issue_id, author, title, description, labels, is_pull_request)

    def get_issue(self, repo_dir: str, issue_id: int) -> Issue:
        """ Gets an issue record from the repository.

        Args:
            repo_dir (str): The issue repository.
            issue_id (int): The issue identifier.

        Raises:
            ValueError: Thrown when missing repo_dir.

        Returns:
            Issue: The issue.
        """
        if not repo_dir or issue_id is None:
            raise ValueError(
                "You cannot get an issue without a repo_dir and an issue_id.")
        session: Schema = self.get_schema()
        return Issues.get_issue(session, repo_dir, issue_id)

    def get_issues(self,
                   repo_dir: str = None,
                   author: str = None,
                   pull_requests: bool = True) -> List[Issue]:
        """ Gets a list of issues.

        Args:
            repo_dir (str, optional): The issues repository. Defaults to None.
            author (str, optional): The issues author. Defaults to None.
            pull_requests (bool, optional): If set to False,
                it returns the matching issues,including pull requests. Defaults to True.

        Returns:
            List[Issue]: List of issues.
        """
        session: Schema = self.get_schema()
        return Issues.get_issues(session, repo_dir, author, pull_requests)

    def create_task(self, repo_dir: str, task_type: TaskType, params: dict = None) -> Task:
        """ Creates a new task.

        Args:
            repo_dir (str): The task repository.
            task_type (TaskType): The task type.

        Raises:
            ValueError: Thrown when missing repo_dir.

        Returns:
            Task: The task.
        """
        if not repo_dir or task_type is None:
            raise ValueError(
                "You cannot create a task without a repo_dir and a task_type.")
        session: Schema = self.get_schema()
        return Tasks.create(
            session, TaskState.QUEUED, datetime.utcnow(), repo_dir, task_type, params)

    def get_task(self, task_id: int) -> Task:
        """ Gets the task record with that task_id.

        Args:
            session (Session): The database session.
            task_id (int): The task id.

        Raises:
            ValueError: Thrown when missing task_id.

        Returns:
            Task: The task.
        """
        if task_id is None:
            raise ValueError("You cannot get a task without a task_id.")
        session: Schema = self.get_schema()
        return Tasks.get_task(session, task_id)

    def get_tasks(self, repo_dir: str = None, task_state: TaskState = None) -> List[Task]:
        """ Gets a list of tasks.

        Args:
            session (Session): The database session.
            repo_dir (str, optional): The task repository. Defaults to None.
            task_state (TaskState, optional): The task state. Defaults to None.

        Returns:
            List[Task]: List of tasks.
        """
        session: Schema = self.get_schema()
        return Tasks.get_tasks(session, repo_dir, task_state)

    def get_latest_task_from_repo(self,
                                  repo_dir: str,
                                  task_type: TaskType = None,
                                  task_state: TaskState = None) -> Task:
        """ Gets the latest task record with that repo_dir.

        Args:
            repo_dir (str): The task repository.
            task_type (TaskType, optional): The task type. Defaults to None.
            task_state (TaskState, optional): The task state. Defaults to None.

        Raises:
            ValueError:
                Thrown when missing repo_dir.

        Returns:
            List[Task]: List of tasks.
        """
        if not repo_dir:
            raise ValueError(
                "You cannot get the lastest task from an unknown repo_dir.")
        session: Schema = self.get_schema()
        return Tasks.get_latest_task_from_repo(session, repo_dir, task_type, task_state)

    def get_oldest_task_with_state(self, task_type: TaskType, task_state: TaskState) -> Task:
        """ Gets the oldest queued task record.

        Args:
            task_type (TaskType): The task type.
            task_state (TaskState): The task state.

        Raises:
            ValueError:
                Thrown when missing task_type or task_state.

        Returns:
            Task: The oldest queued task with that type and state.
        """
        if task_type is None or task_state is None:
            raise ValueError(
                "You cannot get the oldest task without a task_type and a task_state.")
        session: Schema = self.get_schema()
        return Tasks.get_oldest_task_with_state(session, task_type, task_state)

    def update_task_state(self, task_id: int, task_state: TaskState) -> None:
        """ Updates the state of a task.

        Args:
            task_id (str): The task id.
            task_state (TaskState): The task state.

        Raises:
            ValueError:
                Thrown when missing task_id or task_state.
        """
        if task_id is None or task_state is None:
            raise ValueError(
                "You cannot get the update the state of a task "
                "without a task_id and a task_state.")
        session: Schema = self.get_schema()
        return Tasks.update_task_state(session, task_id, task_state)

    def update_task_type(self, task_id: int, task_type: TaskType, params: dict = None) -> None:
        """ Updates the type of a task and his parameters if needed.

        Args:
            task_id (str): The task id.
            task_type (int): The task type.
            params (str, optional): The task parameters.

        Raises:
            ValueError:
                Thrown when missing task_id or task_type.
        """
        if task_id is None or task_type is None:
            raise ValueError(
                "You cannot get the update the type of a task "
                "without a task_id and a task_type.")
        session: Schema = self.get_schema()
        return Tasks.update_task_type(session, task_id, task_type, params)

    def create_comment(self,
                       repo_dir: str,
                       issue_id: int,
                       comment_id: int,
                       author: str,
                       body: str) -> Comment:
        """ Creates a new Comment record.

        Args:
            repo_dir (str): The issue repository.
            issue_id (int): The issue identifier.
            comment_id (int): The comment identifier.
            author (str): The comment author.
            body (str): The comment body.

        Raises:
            ValueError: Thrown when missing repo_dir, issue_id, comment_id or author.

        Returns:
            Comment: The comment.
        """
        if not repo_dir or issue_id is None or comment_id is None or not author:
            raise ValueError(
                "You cannot create an issue without a repo_dir, "
                "an issue_id, a comment_id and an author.")
        session: Schema = self.get_schema()
        return Comments.create(session, repo_dir, issue_id, comment_id, author, body)

    def get_comment(self, repo_dir: str, issue_id: int, comment_id: int) -> Comment:
        """ Gets a Comment record from the repository.

        Args:
            repo_dir (str): The issue repository.
            issue_id (int): The issue identifier.
            comment_id (int): The comment identifier.

        Raises:
            ValueError:
                Thrown when there isn't any comment with that
                repo_dir, issue_id and comment_id in the database records.

        Returns:
            Comment: The comment.
        """
        if not repo_dir or issue_id is None or comment_id is None:
            raise ValueError(
                "You cannot get an issue without a repo_dir, an issue_id and a comment_id.")
        session: Schema = self.get_schema()
        return Comments.get_comment(session, repo_dir, issue_id, comment_id)

    def get_comments(self,
                     repo_dir: str = None,
                     issue_id: int = None,
                     author: str = None) -> List[Comment]:
        """ Gets a list of comments.

        Args:
            repo_dir (str, optional): The issue repository. Defaults to None.
            issue_id (int, optional): The comment identifier. Defaults to None.
            author (str, optional): The comments author. Defaults to None.

        Returns:
            List[Comment]: List of comments.
        """
        session: Schema = self.get_schema()
        return Comments.get_comments(session, repo_dir, issue_id, author)

    def create_outcome(self,
                       task_id: int,
                       repo_dir: str,
                       model_type: str,
                       outcome_data: dict,
                       exec_time: float) -> Outcome:
        """ Creates a new Outcome record.

        Args:
            session (Session): The database session.
            task_id (int): The task id.
            repo_dir (str): The task repository.
            model_type (str): The model type.
            outcome_data (dict): The task outcome.
            exec_time (float): The task execution time.

        Raises:
            ValueError: Thrown when missing task_id, repo_dir,
                model_type, outcome_data or exec_time.

        Returns:
            Outcome: The outcome.
        """
        if (task_id is None or not repo_dir or
                not model_type or outcome_data is None or exec_time is None):
            raise ValueError(
                "You cannot create an outcome without a task_id, a repo_dir, "
                "a model_type, an outcome_data and an exec_time.")
        session: Schema = self.get_schema()
        return Outcomes.create(session, task_id, repo_dir, model_type, outcome_data, exec_time)

    def get_outcome(self, task_id: int) -> Outcome:
        """ Gets a Outcome record from the repository.

        Args:
            session (Session): The database session.
            task_id (int): The task id.

        Raises:
            ValueError: Thrown when missing task_id.

        Returns:
            Outcome: The outcome.
        """
        if task_id is None:
            raise ValueError(
                "You cannot get an outcome without a task_id.")
        session: Schema = self.get_schema()
        return Outcomes.get_outcome(session, task_id)

    def get_outcomes(self,
                     repo_dir: str = None,
                     model_type: str = None) -> List[Outcome]:
        """ Gets a list of outcomes.

        Args:
            session (Session): The database session.
            repo_dir (str, optional): The outcome repository. Defaults to None.
            model_type (str, optional): The model type. Defaults to None.

        Returns:
            List[Outcome]: List of outcomes.
        """
        session: Schema = self.get_schema()
        return Outcomes.get_outcomes(session, repo_dir, model_type)
