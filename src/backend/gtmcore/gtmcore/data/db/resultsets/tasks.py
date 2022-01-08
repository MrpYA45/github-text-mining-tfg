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

""" Tasks class module.
"""

import json
from datetime import datetime
from typing import List, Optional

from gtmcore.data.db.enums import TaskState, TaskType
from gtmcore.data.db.err import TaskAlreadyExistsError, TaskNotExistsError
from gtmcore.data.db.results.task import Task
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.query import Query  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore


class Tasks():
    """ Class responsible of table-level logs operations for Tasks.
    """
    @staticmethod
    def create(session: Session, state: TaskState, timestamp: datetime,
               repo_dir: str, task_type: TaskType, params: dict = None) -> Task:
        """ Creates a new Task record.

        Args:
            session (Session): The database session.
            state (TaskState): The task state.
            timestamp (datetime): The time when the task was created.
            repo_dir (str): The task repository.
            task_type (TaskType): The task type.
            params (str, optional): The task parameters. Defaults to None.

        Raises:
            ValueError: Thrown when missing status, timestamp or repo_dir.
            TaskAlreadyExistsError: Thrown when already exists a task with the same task_id.

        Returns:
            Task: The task.
        """
        if state is None or not timestamp or not repo_dir or task_type is None:
            raise ValueError(
                "You cannot create a task without a status, a timestamp and a repo_dir.")
        try:
            params_1: str = json.dumps(params)
            task: Task = Task(state.value, timestamp,
                              repo_dir, task_type.value, params_1)
            session.add(task)
            session.commit()
            return task
        except IntegrityError as err:
            raise TaskAlreadyExistsError from err

    @staticmethod
    def get_task(session: Session, task_id: int) -> Task:
        """ Gets the task record with that repo_dir.

        Args:
            session (Session): The database session.
            task_id (int): The task id.

        Raises:
            TaskNotExistsError:
                Thrown when there isn't any task with that repo_dir in the database records.

        Returns:
            Task: The task.
        """
        query: Query = session.query(Task).filter_by(task_id=task_id)
        task: Optional[Task] = query.first()
        if task is None:
            raise TaskNotExistsError
        return task

    @staticmethod
    def get_tasks(session: Session, repo_dir: str = None,
                  state: TaskState = None, task_type: TaskType = None) -> List[Task]:
        """ Gets a list of tasks.

        Args:
            session (Session): The database session.
            repo_dir (str, optional): The task repository. Defaults to None.
            state (TaskState, optional): The task state. Defaults to None.
            task_type (TaskType, optional): The task type. Defaults to None.

        Returns:
            List[Task]: List of tasks.
        """
        query: Query = session.query(Task)
        if repo_dir is not None:
            query = query.filter_by(repo_dir=repo_dir)
        if state is not None:
            query = query.filter_by(state=state.value)
        if task_type is not None:
            query = query.filter_by(task_type=task_type.value)
        return query.all()

    @staticmethod
    def get_latest_task_from_repo(
            session: Session,
            repo_dir: str,
            task_type: TaskType = None,
            state: TaskState = None) -> Task:
        """ Gets the latest task record with that repo_dir.

        Args:
            session (Session): The database session.
            repo_dir (str): The task repository. Defaults to None.
            task_type (TaskType, optional): The task type. Defaults to None.
            state (TaskState, optional): The task state. Defaults to None.

        Raises:
            TaskNotExistsError:
                Thrown when there isn't any task with that repo_dir in the database records.

        Returns:
            List[Task]: List of tasks.
        """
        query: Query = session.query(Task).filter_by(repo_dir=repo_dir)
        if task_type is not None:
            query = query.filter_by(task_type=task_type.value)
        if state is not None:
            query = query.filter_by(state=state.value)
        task: Optional[Task] = query.order_by(
            getattr(Task, "timestamp").desc()).first()
        if task is None:
            raise TaskNotExistsError
        return task

    @staticmethod
    def get_oldest_task_with_state(session: Session, task_type: TaskType, state: TaskState) -> Task:
        """ Gets the oldest queued task record.

        Args:
            session (Session): The database session.
            task_type (TaskType): The task type.
            state (TaskState): The task state.

        Raises:
            TaskNotExistsError:
                Thrown when there isn't any task with that state in the database records.

        Returns:
            Task: The oldest queued task.
        """
        query: Query = session.query(Task).filter_by(
            state=state.value, task_type=task_type.value).order_by("timestamp")
        task: Optional[Task] = query.first()
        if task is None:
            raise TaskNotExistsError
        return task

    @staticmethod
    def update_task_state(session: Session, task_id: int, state: TaskState) -> None:
        """ Updates the state of a task.

        Args:
            session (Session): The database session.
            task_id (int): The task id.
            state (TaskState): The task state.

        Raises:
            TaskNotExistsError:
                Thrown when there isn't any task with that task_id in the database records.
        """
        try:
            task: Task = Tasks.get_task(session, task_id)
            task.state = state.value
            session.commit()
        except IntegrityError as err:
            session.rollback()
            raise TaskNotExistsError from err

    @staticmethod
    def update_task_type(session: Session, task_id: int,
                         task_type: TaskType, params: dict = None) -> None:
        """ Updates the type of a task and his parameters if needed.

        Args:
            session (Session): The database session.
            task_id (int): The task id.
            task_type (int): The task type.
            params (str, optional): The task parameters.

        Raises:
            TaskNotExistsError:
                Thrown when there isn't any task with that task_id in the database records.
        """
        try:
            task: Task = Tasks.get_task(session, task_id)
            task.task_type = task_type.value
            task.params = json.dumps(params)
            session.commit()
        except IntegrityError as err:
            raise TaskNotExistsError from err
