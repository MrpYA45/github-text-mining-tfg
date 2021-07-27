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

import json
import logging
from typing import Dict, List, Tuple, Union

from gtmcore.data.db.results import Comment, Issue, Repository, Task
from gtmcore.logic.dbmanager import DBManager
from gtmprocessing.logic.models import (SentimentsAnalysis, Summarization,
                                        ZeroShotClassifier)

TaskArgsType = Union[str, int, List[int], List[str]]


class ProcessingManager():
    def __init__(self, db_manager: DBManager) -> None:
        self.__dbmanager: DBManager = db_manager
        self.__zeroshotclassifier: ZeroShotClassifier = ZeroShotClassifier()
        self.__summarization: Summarization = Summarization()
        self.__sentimentsanalysis: SentimentsAnalysis = SentimentsAnalysis()

    def process_task(self, task: Task) -> None:
        logging.debug(
            "[GTMProcessing] STARTING TASK PROCESSING. TASK ID: %s | REPO: %s | TASK_TYPE: %s | PARAMS: %s",
            task.task_id, task.repo_dir, task.task_type, json.dumps(task.params))
        print("[GTMProcessing] STARTING TASK PROCESSING. TASK ID: %s | REPO: %s | TASK_TYPE: %s | PARAMS: %s" % (task.task_id, task.repo_dir, task.task_type, json.dumps(task.params)))

        params: Dict[str, TaskArgsType] = json.load(task.params)
        model_type: str = params.get("model_type")

        model_outcome: dict
        exec_time: float
        model_outcome, exec_time = self.apply_model(
            task.repo_dir, model_type, params)
        print("[GTMProcessing] ENDING TASK PROCESSING FROM REPO: %s | RESULTS: %s" % (task.repo_dir, str(model_outcome)))
        logging.debug(
            "[GTMProcessing] ENDING TASK PROCESSING FROM REPO: %s | RESULTS: %s",
            task.repo_dir, str(model_outcome))

        self.__dbmanager.create_outcome(
            task.task_id, task.repo_dir, model_type, model_outcome, exec_time)

    def apply_model(self, repo_dir: str, model_type: str, params: Dict[str, TaskArgsType]) -> List[Dict[str, TaskArgsType]]:
        if model_type == "zsc":
            return self.apply_zeroshotclassifier(*self.get_zsc_params(repo_dir, params))
        if model_type == "summ":
            return self.apply_summarization(*self.get_summ_params(repo_dir, params))
        if model_type == "sa":
            return self.apply_sentimentanalisys(*self.get_sa_params(repo_dir, params))

    def get_zsc_params(self, repo_dir: str, params: Dict[str, TaskArgsType]) -> Tuple[TaskArgsType]:
        issue_id: int = params.get("issue_id", None)
        accuracy: float = params.get("accuracy", 0.7)
        use_desc: bool = params.get("use_desc", False)
        extra_tags: List[str] = params.get("extra_tags", None)
        return (repo_dir, issue_id, accuracy, use_desc, extra_tags)

    def get_summ_params(self, repo_dir: str, params: Dict[str, TaskArgsType]) -> Tuple[TaskArgsType]:
        issue_id: int = params.get("issue_id", None)
        with_comments: bool = params.get("with_comments", False)
        max_length: int = params.get("max_length", 150)
        min_length: int = params.get("min_length", 50)
        return (repo_dir, issue_id, with_comments, max_length, min_length)

    def get_sa_params(self, repo_dir: str, params: Dict[str, TaskArgsType]) -> Tuple[TaskArgsType]:
        issue_id: int = params.get("issue_id", None)
        author: str = params.get("author", None)
        with_comments: bool = params.get("with_comments", False)
        return (repo_dir, issue_id, author, with_comments)

    def apply_zeroshotclassifier(self,
                                 repo_dir: str,
                                 issue_id: int,
                                 accuracy: float,
                                 use_desc: bool,
                                 extra_tags: List[str]) -> List[Dict[str, TaskArgsType]]:

        repo: Repository = self.__dbmanager.get_repository(repo_dir)
        labels: List[str] = json.load(repo.labels)

        labels += extra_tags

        issue: Issue = self.__dbmanager.get_issue(repo_dir, issue_id)
        text: List[str] = [issue.title]

        if use_desc:
            text += (" ", issue.description)

        data: dict = {
            "accuracy": accuracy,
            "labels": labels,
            "text": text
        }
        return self.__zeroshotclassifier.apply(data)

    def apply_summarization(self,
                            repo_dir: str,
                            issue_id: int,
                            with_comments: bool,
                            max_length: int,
                            min_length: int) -> List[Dict[str, TaskArgsType]]:

        issue: Issue = self.__dbmanager.get_issue(repo_dir, issue_id)
        texts: List[str] = [issue.description]

        if with_comments:
            comments: List[Comment] = self.__dbmanager.get_comments(
                repo_dir, issue_id)
            texts += [comment.body for comment in comments]

        data: dict = {
            "max_length": max_length,
            "min_length": min_length,
            "texts": texts
        }
        return self.__summarization.apply(data)

    def apply_sentimentanalisys(self,
                                repo_dir: str,
                                issue_id: int,
                                author: str,
                                with_comments: bool) -> List[Dict[str, TaskArgsType]]:

        issues: List[Issue] = self.__dbmanager.get_issues(repo_dir, author)

        for issue in issues:
            texts: List[str] = [issue.description]

            if with_comments:
                comments: List[Comment] = self.__dbmanager.get_comments(
                    repo_dir, issue_id, author)
                texts += [comment.body for comment in comments]

        data: dict = {
            "texts": texts
        }
        return self.__sentimentsanalysis.apply(data)
