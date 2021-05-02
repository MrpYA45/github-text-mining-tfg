""" Tasks class module.
"""

from datetime import datetime
from typing import List, Optional

from github_text_mining.github_text_mining.data.db.err.taskalreadyexistserror import \
    TaskAlreadyExistsError
from github_text_mining.github_text_mining.data.db.err.tasknotexistserror import \
    TaskNotExistsError
from github_text_mining.github_text_mining.data.db.results.task import Task
from github_text_mining.github_text_mining.data.db.taskstate import TaskState
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.query import Query  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy.sql.schema import Sequence  # type: ignore


class Tasks():
    """ Class responsible of table-level logs operations for Tasks
    """
    @staticmethod
    def create(session: Session, state: TaskState, timestamp: datetime, repo_dir: str) -> Task:
        """ Creates a new Task record.

        Args:
            session (Session): The database session.
            state (int): The task state.
            timestamp (datetime): The time when the task was created.
            repo_dir (str): The task repository.

        Raises:
            ValueError: Thrown when missing status, timestamp or repo_dir.
            TaskAlreadyExistsError: Thrown when already exist a task with the same task_id.

        Returns:
            Task: The task.
        """
        if state is None or not timestamp or not repo_dir:
            raise ValueError(
                "You cannot create a task without a status, a timestamp and a repo_dir.")
        try:
            task: Task = Task(state.value, timestamp, repo_dir)
            session.add(task)
            session.commit()
            return task
        except IntegrityError:
            raise TaskAlreadyExistsError

    @staticmethod
    def set_task_state(session: Session, repo_dir: str, state: TaskState) -> None:
        try:
            task: Task = Tasks.get_task(session, repo_dir)
            task.state = state.value
            session.commit()
        except IntegrityError:
            raise TaskNotExistsError

    @staticmethod
    def get_task(session: Session, repo_dir: str) -> Task:
        """ Gets the lastest task record with that repo_dir.

        Args:
            session (Session): The database session.
            repo_dir (str): The task repository.

        Raises:
            TaskNotExistsError:  Thrown when there isn't any task with that repo_dir in the database records.

        Returns:
            Task: The task.
        """
        query: Query = session.query(Task).filter_by(repo_dir=repo_dir)
        task: Optional[Task] = query.first()
        if task is None:
            raise TaskNotExistsError
        return task

    @staticmethod
    def get_next_queued_task(session: Session) -> Task:
        query: Query = session.query(Task).filter_by(
            state=TaskState.Queued.value).order_by(Task.timestamp)
        task = query.first()
        return task

    @staticmethod
    def get_tasks(session: Session, repo_dir: str = None, state: TaskState = None) -> List[Task]:
        """ Gets a list of tasks.

        Args:
            session (Session): The database session.
            repo_dir (str, optional): The task repository. Defaults to None.
            state (TaskState, optional): The task state. Defaults to None.

        Returns:
            List[Task]: List of tasks.
        """
        query: Query = session.query(Task)
        if repo_dir is not None:
            query = query.filter_by(repo_dir=repo_dir)
        if state is not None:
            query = query.filter_by(state=state.value)
        return query.all()
