import json
from datetime import datetime

from data.db import DBManager, Schema
from logic.connections import GitHubConnection, GitHubManager
from logic.connections.config import ConnConfiguration
from logic.taskmanager import TaskManager


def run():
    url = "https://github.com/MrpYA45/github-text-mining-tfg"
    repo_dir: str = GitHubManager.get_repo_dir(url)
    db = Schema()
    ConnConfiguration()
    
    gh_conn = GitHubConnection()
    task_manager = TaskManager(db, gh_conn)
    
    task_manager.add_task(repo_dir)
    task_manager.capture_repo_data(repo_dir)

if __name__ == "__main__":
    run()
