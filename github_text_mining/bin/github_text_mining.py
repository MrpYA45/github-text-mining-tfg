#!/usr/bin/env python3
import logging
from multiprocessing.context import Process

from flask import Flask, json, jsonify, render_template, request
from flask.logging import default_handler

from github_text_mining.github_text_mining.data.db.schema import Schema
from github_text_mining.github_text_mining.logic.connections.config.connconfiguration import \
    ConnConfiguration
from github_text_mining.github_text_mining.logic.connections.githubconnection import \
    GitHubConnection
from github_text_mining.github_text_mining.logic.connections.githubmanager import \
    GitHubManager
from github_text_mining.github_text_mining.logic.dbmanager import DBManager
from github_text_mining.github_text_mining.logic.processes.data_extractor_process import \
    DataExtractorProcess
from github_text_mining.github_text_mining.presentation.rest.taskmanager import \
    TaskManager

app = Flask(__name__)
root_logger = logging.getLogger()
root_logger.addHandler(default_handler)

config = ConnConfiguration()
schema: Schema = Schema()
db_manager: DBManager = DBManager(schema)
gh_conn: GitHubConnection = GitHubConnection()
gh_manager: GitHubManager = GitHubManager(gh_conn, db_manager)
task_manager: TaskManager = TaskManager(db_manager)


@app.route("/", methods=["GET"])
def is_running():
    # ("", 200, {"Content-Type": "text/plain"})
    return render_template("index.html")


@app.route("/tasks/", methods=["GET"])
def get_all_tasks():
    tasks = task_manager.get_tasks()
    return jsonify(eqtls=[str(task) for task in tasks])


@app.route("/task/<string:repo_user>/<string:repo_name>", methods=["GET", "POST"])
def create_task(repo_user: str, repo_name: str):
    repo_dir: str = repo_user + "/" + repo_name
    if request.method == "POST":
        task_added = task_manager.add_task(repo_dir)
        response = app.response_class(
            response=json.dumps({"Añadido": task_added}),
            status=200,
            mimetype='application/json'
        )
    else:
        repo_dir = GitHubManager.get_repo_dir(repo_dir)
        task = task_manager.get_task(repo_dir)
        response = app.response_class(
            response=jsonify(str(task)),
            status=200,
            mimetype='application/json'
        )
    return response


@app.route("/test/", methods=["POST"])
def test_task():
    res = task_manager.add_task(
        "https://github.com/MrpYA45/github-text-mining-tfg/")
    response = app.response_class(
        response=json.dumps({"Test": res}),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6060, debug=True)
