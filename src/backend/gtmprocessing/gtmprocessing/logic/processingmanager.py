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
from typing import Dict, List, Union
from gtmcore.data.db.err.repositorynotexistserror import RepositoryNotExistsError

from gtmcore.data.db.results import Task
from gtmcore.logic.dbmanager import DBManager
from gtmprocessing.data.err.invalidnlpmodel import InvalidNLPModel
from gtmprocessing.logic.models import (SentimentsAnalysis, Summarization,
                                        ZeroShotClassifier)
from gtmprocessing.logic.models.basemodel import BaseModel

TaskArgsType = Union[str, int, List[int], List[str]]


class ProcessingManager():

    def __init__(self, db_manager: DBManager) -> None:
        self.__dbmanager: DBManager = db_manager

        self.__models_types: Dict[str, BaseModel] = {
            "zsc": ZeroShotClassifier(self.__dbmanager),
            "summ": Summarization(self.__dbmanager),
            "sa": SentimentsAnalysis(self.__dbmanager)
        }

    def process_task(self, task: Task) -> bool:
        try:
            # pylint: disable=line-too-long
            logging.debug(
                "[GTMProcessing] STARTING TASK PROCESSING. TASK ID: %s | REPO: %s | TASK_TYPE: %s | PARAMS: %s",
                task.task_id, task.repo_dir, task.task_type, json.dumps(task.params))
            
            if self.__dbmanager.get_repository(task.repo_dir) is None:
                raise RepositoryNotExistsError

            params: Dict[str, TaskArgsType] = json.loads(task.params)
            model_type: str = str(params.get("model_type", ""))

            nlp_model: BaseModel = self.__models_types[model_type]

            params["repo_dir"] = task.repo_dir

            nlp_model.set_params(params)
            logging.debug(
                "[GTMProcessing] TASK PROCESSING. PARAMETERS SET. TASK ID: %s | REPO: %s | TASK_TYPE: %s | PARAMS: %s",
                task.task_id, task.repo_dir, task.task_type, json.dumps(task.params))
            nlp_model.preprocess()
            logging.debug(
                "[GTMProcessing] TASK PROCESSING. PREPROCESSING MADE. TASK ID: %s | REPO: %s | TASK_TYPE: %s | PARAMS: %s",
                task.task_id, task.repo_dir, task.task_type, json.dumps(task.params))
            nlp_model.apply()
            logging.debug(
                "[GTMProcessing] TASK PROCESSING. NLP MODEL APPLIED. TASK ID: %s | REPO: %s | TASK_TYPE: %s | PARAMS: %s",
                task.task_id, task.repo_dir, task.task_type, json.dumps(task.params))

            model_outcome: Dict[str, TaskArgsType]
            exec_time: float
            model_outcome, exec_time = nlp_model.get_outcome()

            logging.debug(
                "[GTMProcessing] ENDING TASK PROCESSING FROM REPO: %s | RESULTS: %s | EXECUTION TIME: %f",
                task.repo_dir, json.dumps(model_outcome), exec_time)

            self.__dbmanager.create_outcome(
                task.task_id, task.repo_dir, model_type, model_outcome, exec_time)

            return True
        except KeyError as err:
            raise InvalidNLPModel from err
