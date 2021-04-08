import json
from datetime import datetime
from .data.db.results.task import Task
from .data.db import Schema
from .logic import DBManager
from .logic.connections import GitHubConnection, GitHubManager


def run():
    token = ""
    url = "https://github.com/MrpYA45/github-text-mining-tfg"
    db = Schema()
    manager = DBManager(db)
    gh_conn = GitHubConnection()
    gh_conn.create_session(token)
    github = GitHubManager(gh_conn, manager)
    manager.create_task(datetime.utcnow(), url)
    manager.create_task(datetime.utcnow(), url)
    manager.create_task(datetime.utcnow(), url)
    manager.create_task(datetime.utcnow(), url)
    dbtask = manager.get_tasks()
    print("TAREA: " + json.dumps(str(dbtask[2])))
    repo_dir = github.get_repo_dir(url)
    github.add_repo_info_into_db(repo_dir)
    github.add_issues_info_into_db(repo_dir)
    dbrepo = manager.get_repositories()
    print("REPO: " + json.dumps(str(dbrepo[0])))
    dbissues = manager.get_issues(repo_dir)
    for dbissue in dbissues:
        print("ISSUE: " + json.dumps(str(dbissue)) + "\n\n\n")


if __name__ == "__main__":
    run()
