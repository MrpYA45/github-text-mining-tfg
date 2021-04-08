""" Tasks class module.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.schema import Sequence  # type: ignore
from ..results.task import Task


class Tasks():
    """ Class responsible of table-level logs operations for Tasks
    """
    @staticmethod
    def create(session: Session, state: int, timestamp: datetime, url: str) -> Task:
        if state is None or not timestamp or not url:
            raise ValueError(
                "You cannot create a task without a status, a timestamp and a url.")
        try:
            task = Task(state, timestamp, url)
            session.add(task)
            session.commit()
            return task
        except IntegrityError:
            raise NotImplementedError

    @staticmethod
    def get_task(session: Session, task_id: int) -> Task:
        query = session.query(Task).filter_by(task_id=task_id)
        task: Optional[Task] = query.first()
        if task is None:
            raise NotImplementedError
        return task

    @staticmethod
    def get_tasks(session: Task, state: str = None) -> List[Task]:
        query = session.query(Task)
        if state is not None:
            query.filter_by(state=state)
        return query.all()
