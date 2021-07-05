import json
import logging
from typing import List

from gtmcore.data.db.results import Task
from gtmcore.data.db.results.issue import Issue
from gtmcore.data.db.results.repository import Repository
from gtmcore.logic.dbmanager import DBManager
from gtmprocessing.logic.models.sentimentsanalysis import SentimentsAnalysis
from gtmprocessing.logic.models.summarization import Summarization
from gtmprocessing.logic.models.zeroshotclassifier import ZeroShotClassifier


class ProcessingManager():
    def __init__(self, db_manager: DBManager) -> None:
        self.__dbmanager: DBManager = db_manager
        self.__zeroshotclassifier: ZeroShotClassifier = ZeroShotClassifier()
        self.__summarization: Summarization = Summarization()
        self.__sentimentsanalysis: SentimentsAnalysis = SentimentsAnalysis()

    def process_task(self, task: Task) -> bool:
        logging.debug(
            "[GTMProcessing] STARTING TASK PROCESSING. TASK ID: %s | REPO: %s | ALGORITHM: %s",
            task.task_id, task.repo_dir, task.task_type)
        results: List[dict] = self.apply_zeroshotclassifier(
            task)
        logging.debug(
            "[GTMProcessing] ENDING TASK PROCESSING FROM REPO: %s | RESULTS: %s",
            task.repo_dir, str(results))
        return True

    def apply_zeroshotclassifier(self, task: Task) -> List[dict]:
        repo: Repository = self.__dbmanager.get_repository(task.repo_dir)
        issues: List[Issue] = self.__dbmanager.get_issues(task.repo_dir)
        data: dict = {
            "labels": json.loads(repo.labels),
            "sequences": [issue.title for issue in issues]
        }

        return self.__zeroshotclassifier.apply(data)

    def apply_summarization(self, task: Task) -> List[dict]:
        repo: Repository = self.__dbmanager.get_repository(task.repo_dir)
        issues: List[Issue] = self.__dbmanager.get_issues(
            task.repo_dir, pull_requests=False)
        data: dict = {

        }
        return self.__summarization.apply(data)

    def apply_sentimentanalisys(self, task: Task) -> List[dict]:
        repo: Repository = self.__dbmanager.get_repository(task.repo_dir)
        issues: List[Issue] = self.__dbmanager.get_issues(
            task.repo_dir, pull_requests=False)
        data: dict = {

        }
        return self.__sentimentsanalysis.apply(data)
