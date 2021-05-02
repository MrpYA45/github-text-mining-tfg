import time
from multiprocessing import Process

from github_text_mining.github_text_mining.data.db.results.task import Task
from github_text_mining.github_text_mining.data.db.schema import Schema
from github_text_mining.github_text_mining.data.db.taskstate import TaskState
from github_text_mining.github_text_mining.logic.connections import (
    GitHubConnection, GitHubManager)
from github_text_mining.github_text_mining.logic.dbmanager import DBManager


class DataExtractorProcess(Process):

    def __init__(self):
        super(DataExtractorProcess, self).__init__()
        schema: Schema = Schema()
        db_manager: DBManager = DBManager(schema)
        gh_conn: GitHubConnection = GitHubConnection()
        gh_manager: GitHubManager = GitHubManager(gh_conn, db_manager)
        self.db_manager = db_manager
        self.gh_manager = gh_manager

    def run(self):
        while True:
            print("Running")
            task = self.get_next_queued_task()
            if task:
                self.db_manager.set_task_state(
                    task.repo_dir, TaskState.CapturingData)
                self.capture_repo_data(task.repo_dir)
                self.db_manager.set_task_state(
                    task.repo_dir, TaskState.Waiting)
            time.sleep(1)

    def capture_repo_data(self, repo_dir: str) -> bool:
        self.__running = True
        title, description = self.gh_manager.get_repo_info(repo_dir)
        self.db_manager.create_repository(repo_dir, title, description)

        issues_data = self.gh_manager.get_repo_issues(repo_dir)
        for issue_data in issues_data:
            self.db_manager.create_issue(
                repo_dir,
                issue_data["id"],
                issue_data["title"],
                issue_data["description"],
                issue_data["labels"],
                issue_data["comments"],
                issue_data["isPullRequest"])
        return True

    def get_next_queued_task(self) -> Task:
        return self.db_manager.get_next_queued_task()
