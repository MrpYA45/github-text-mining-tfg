from typing import List

from gtmcore.data.db import TaskState
from gtmcore.data.db.err.tasknotexistserror import TaskNotExistsError
from gtmcore.data.db.results.task import Task
from gtmcore.logic.dbmanager import DBManager


class TaskManager():

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager

    def add_task(self, repo_dir: str) -> bool:
        self.invalidate_old_task(repo_dir)
        try:
            self.db_manager.create_task(repo_dir)
            return True
        except ValueError:
            return False

    def get_task(self, repo_dir: str) -> Task:
        task: Task = self.db_manager.get_task(repo_dir)
        return task

    def get_tasks(self, repo_dir: str = None, state: TaskState = None) -> List[Task]:
        tasks: List[Task] = self.db_manager.get_tasks(repo_dir, state)
        return tasks

    def invalidate_old_task(self, repo_dir: str) -> None:
        self.update_task_state(repo_dir, TaskState.OUTDATED)

    def update_task_state(self, repo_dir: str, state: TaskState) -> bool:
        try:
            self.db_manager.set_task_state(repo_dir, state)
            return True
        except TaskNotExistsError:
            return False
