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

""" Zero-Shot Classifier Module
"""

import json
import time
from typing import Any, Dict, List

import numpy as np
from transformers.pipelines.base import Pipeline  # type: ignore
from gtmcore.data.db.results.issue import Issue
from gtmcore.data.db.results.repository import Repository
from gtmcore.logic.dbmanager import DBManager
from gtmprocessing.logic.models.basemodel import BaseModel

class ZeroShotClassifier(BaseModel):
    """ Class in charge of applying the NLP ZeroS-hot Classifier model.
    """
    # pylint: disable=too-many-instance-attributes

    def __init__(self, dbmanager: DBManager) -> None:
        super().__init__()
        self.__dbmanager: DBManager = dbmanager
        self.__pipeline: Pipeline = self.get_pipeline()

        self.__accuracy:  float = 0.0
        self.__use_desc:  bool = False
        self.__labels:  List[str] = []

    def set_params(self, params: Dict[str, Any]) -> None:
        super().set_params(params)

        self.__accuracy = float(params.get("accuracy", 0.7))
        self.__use_desc = bool(params.get("use_desc", False))
        self.__labels = params.get("extra_labels", [])

    def preprocess(self) -> None:
        try:
            repo: Repository = self.__dbmanager.get_repository(self._repo_dir)
            repo_labels: List[str] = json.loads(repo.labels)

            self.__labels += repo_labels

            issue: Issue = self.__dbmanager.get_issue(
                self._repo_dir, self._issue_id)
            inputs: List[str] = [issue.title]

            if self.__use_desc:
                inputs += (" ", issue.description)

            self._inputs = self.chunk_input(inputs, self.__pipeline.tokenizer)
        except ValueError as err:
            raise ValueError(
                "Missing, incorrect or damaged model paramethers.") from err

    def apply(self) -> None:

        start_time: float = time.time()

        total_ratings: List[List[float]] = []

        for paragraph in self._inputs:
            ratings: List[float] = self.__pipeline(
                paragraph,
                self.__labels,
                multi_label=True
            ).get("scores", [])
            total_ratings.append(ratings)

        avg_ratings: np.ndarray = np.average(total_ratings, axis=0)

        threshold_indexes: np.ndarray = np.where(avg_ratings > self.__accuracy)

        filtered_labels: np.ndarray = np.array(
            self.__labels)[threshold_indexes]
        filtered_ratings: np.ndarray = avg_ratings[threshold_indexes]

        self._exec_time: float = time.time() - start_time

        self._outcome = {
            "input_chunks": self._inputs,
            "labels": filtered_labels.tolist(),
            "ratings": filtered_ratings.tolist()
        }

    def get_model_str(self) -> str:
        return "zero-shot-classification"
