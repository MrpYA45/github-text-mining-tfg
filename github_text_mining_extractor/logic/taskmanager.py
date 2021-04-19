from datetime import datetime

from data.db import DBManager, Schema, TaskState
from data.db.results.task import Task

from logic.connections import GitHubConnection, GitHubManager
from logic.connections.config import ConnConfiguration


class TaskManager():

    def __init__(self, db: Schema, conn: GitHubConnection) -> None:
        self.db_manager = DBManager(db)
        self.gh_manager = GitHubManager(conn, self.db_manager)

    def add_task(self, repo_dir: str) -> bool:
        self.invalidate_old_tasks(repo_dir)
        try:
            self.db_manager.create_task(repo_dir)
            return True
        except:
            return False

    def capture_repo_data(self, repo_dir: str) -> bool:
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
    
    def invalidate_old_tasks(self, repo_dir) -> None:
        pass

    def update_task_state(self, task: Task, old_state: TaskState, new_state: TaskState) -> bool:
        pass
