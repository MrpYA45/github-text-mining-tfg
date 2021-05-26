""" Database Manager Class Module.
"""

from datetime import datetime
from typing import List, Optional

from gtmcore.data.db import Schema, TaskState
from gtmcore.data.db.err.tasknotexistserror import TaskNotExistsError
from gtmcore.data.db.results import Issue, Repository, Task
from gtmcore.data.db.resultsets import Issues, Repositories, Tasks


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

    def create_task(self, repo_dir: str) -> Task:
        """ Creates a new task.

        Args:
            repo_dir (str): The task repository.

        Raises:
            ValueError: Thrown when missing repo_dir.

        Returns:
            Task: The task.
        """
        if not repo_dir:
            raise ValueError("You cannot create a task without a repo_dir.")
        session = self.get_schema()
        return Tasks.create(session, TaskState.QUEUED, datetime.utcnow(), repo_dir)

    def create_repository(self, repo_dir: str, title: str, description: str) -> Repository:
        """ Creates a new repository.

        Args:
            repo_dir (str): The repository direction.
            title (str): The repository title
            description (str): The repository description.

        Raises:
            ValueError: Thrown when missing repo_dir, title or description.

        Returns:
            Repository: The repository.
        """
        if not repo_dir or not title or not description:
            raise ValueError(
                "You cannot create a repository without a repo_dir, a title and a description.")
        session = self.get_schema()
        return Repositories.create(session, repo_dir, title, description)

    def create_issue(self, repo_dir: str, issue_id: int, title: str, description: str, labels: list,
                     comments: list, is_pull_request: bool) -> Issue:
        """ Creates a new issue.

        Args:
            repo_dir (str): The issue repository.
            issue_id (int): The issue identifier.
            title (str): The issue title.
            description (str): The issue description.
            labels (list): The issue labels.
            comments (dict): The issue comments.
            is_pull_request (bool): If true the issue is a pull request, otherwise false.

        Raises:
            ValueError: Thrown when missing issue_id, repo_dir or title.

        Returns:
            Issue: The issue.
        """
        if not repo_dir or not issue_id or not title:
            raise ValueError(
                "You cannot create an issue without a repo_dir, an issue_id and a title.")
        session = self.get_schema()
        return Issues.create(
            session, repo_dir, issue_id, title, description, labels, comments, is_pull_request)

    def set_task_state(self, repo_dir: str, state: TaskState) -> None:
        """ Updates the state of a task.

        Args:
            repo_dir (str): The task repository.
            state (TaskState): The task state.

        Raises:
            ValueError: Thrown when missing repo_dir or state.
        """
        if not repo_dir or not state:
            raise ValueError(
                "You cannot set the state of an issue without a repo_dir and a state.")
        session = self.get_schema()
        Tasks.set_task_state(session, repo_dir, state)

    def get_task(self, repo_dir: str) -> Task:
        """ Gets the lastest task record with that repo_dir.

        Args:
            session (Session): The database session.
            repo_dir (str): The task repository.

        Raises:
            ValueError: Thrown when missing repo_dir.

        Returns:
            Task: The task.
        """
        if not repo_dir:
            raise ValueError("You cannot get a task without a repo_dir.")
        session = self.get_schema()
        return Tasks.get_task(session, repo_dir)

    def get_next_queued_task(self) -> Optional[Task]:
        session = self.get_schema()
        try:
            return Tasks.get_next_queued_task(session)
        except TaskNotExistsError:
            return None

    def get_tasks(self, repo_dir: str = None, state: TaskState = None) -> List[Task]:
        """ Gets a list of tasks.

        Args:
            session (Session): The database session.
            repo_dir (str, optional): The task repository. Defaults to None.
            state (TaskState, optional): The task state. Defaults to None.

        Returns:
            List[Task]: List of tasks.
        """
        session = self.get_schema()
        return Tasks.get_tasks(session, repo_dir, state)

    def get_repository(self, repo_dir: str) -> Repository:
        """ Gets the repository record.

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
        session = self.get_schema()
        return Repositories.get_repository(session, repo_dir)

    def get_repositories(self) -> List[Repository]:
        """Gets all the repositories.

        Returns:
            List[Repository]: List with all the repositories.
        """
        session = self.get_schema()
        return Repositories.get_repositories(session)

    def get_issue(self, repo_dir: str, issue_id: int) -> Issue:
        """ Gets an issue record from the repository.

        Args:
            repo_dir (str): The issue repository.
            issue_id (int): The issue identifier.

        Raises:
            ValueError: Thrown when missing repo_dir or issue_id.

        Returns:
            Issue: The issue.
        """
        if not repo_dir or not issue_id:
            raise ValueError(
                "You cannot get an issue without a repo_dir and an issue_id.")
        session = self.get_schema()
        return Issues.get_issue(session, repo_dir, issue_id)

    def get_issues(self, repo_dir: str = None, pull_requests=True) -> List[Issue]:
        """ Gets a list of issues.

        Args:
            repo_dir (str, optional): The issue repository. Defaults to None.
            pull_requests (bool, optional): Filters the pull requests. Defaults to True.

        Returns:
            List[Issue]: List of issues.
        """
        session = self.get_schema()
        return Issues.get_issues(session, repo_dir, pull_requests)
