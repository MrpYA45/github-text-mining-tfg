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

import time
from typing import List

import numpy as np
from gtmprocessing.logic.models.basemodel import BaseModel
from gtmprocessing.logic.utils.textpreprocessor import \
    TextPreprocessor  # type: ignore
from transformers.pipelines.base import Pipeline


class ZeroShotClassifier(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.__pipeline: Pipeline = self.get_pipeline()

    def apply(self, data: dict) -> dict:
        accuracy: float = data.get("accuracy")
        labels: List[str] = data.get("labels")
        text: str = data.get("text")

        preprocessor = TextPreprocessor(self.__pipeline.tokenizer)

        sentences: List[str] = preprocessor.preprocess([text])

        total_ratings: List[List[float]] = []

        start_time: float = time.time()

        for sentence in sentences:
            ratings: List[float] = self.__pipeline(
                sentence, labels, multi_label=True).get("scores", [0]*len(labels))
            total_ratings.append(ratings)

        exec_time: float = time.time() - start_time

        avg_ratings: List[float] = np.average(total_ratings, axis=0)

        threshold_indexes: List[float] = np.argwhere(avg_ratings > accuracy)

        filtered_labels = np.array(labels)[threshold_indexes]
        filtered_ratings = avg_ratings[threshold_indexes]

        outcome_data: dict = {
            "labels": filtered_labels,
            "ratings": filtered_ratings
        }

        return outcome_data, exec_time

    def get_model_str(self) -> str:
        return "zero_shot_classification"
