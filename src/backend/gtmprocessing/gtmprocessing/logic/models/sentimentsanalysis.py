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

""" Sentiment Analysis Module.
"""

import time
from typing import Any, Dict, List, Optional

import numpy as np
from transformers import AutoModelForSequenceClassification  # type: ignore
from transformers.pipelines.base import Pipeline  # type: ignore
from gtmcore.data.db.results.comment import Comment
from gtmcore.data.db.results.issue import Issue
from gtmcore.logic.dbmanager import DBManager
from gtmprocessing.logic.models.basemodel import BaseModel


class SentimentsAnalysis(BaseModel):
    """ Class in charge of applying the NLP Sentiment Analysis model.
    """

    def __init__(self, dbmanager: DBManager) -> None:
        super().__init__()
        self.__dbmanager: DBManager = dbmanager
        self.__pipeline: Pipeline = self.get_pipeline()

        self.__author: Optional[str] = None
        self.__with_comments: bool = False

    def set_params(self, params: Dict[str, Any]) -> None:
        super().set_params(params)

        self.__author = str(params.get("author", ""))
        self.__with_comments = bool(params.get("with_comments", False))

    def preprocess(self) -> None:

        inputs: List[str] = []

        issue: Issue = self.__dbmanager.get_issue(
            self._repo_dir, self._issue_id)

        if self.__author == "" or self.__author == issue.author:
            inputs = [issue.title, issue.description]

        if self.__with_comments:
            comments: List[Comment] = self.__dbmanager.get_comments(
                self._repo_dir, self._issue_id, self.__author)
            if self.__author == "":
                inputs += [comment.body for comment in comments]
            else:
                for comment in comments:
                    if comment.author == self.__author:
                        inputs.append(comment.body)

        self._inputs = self.chunk_input(inputs, self.__pipeline.tokenizer)

    def apply(self) -> None:

        start_time: float = time.time()

        sa_scores: List[float] = []

        for paragraph in self._inputs:
            sa_score = self.__pipeline(paragraph)[0].get("score", 0)
            sa_scores.append(sa_score)

        self._exec_time: float = time.time() - start_time

        avg_sa_score: float = float(np.mean(sa_scores))

        self._outcome = {
            "input_chunks": len(self._inputs),
            "sa_scores": sa_scores,
            "avg_sa_score": avg_sa_score
        }

    def get_model(self) -> AutoModelForSequenceClassification:
        return AutoModelForSequenceClassification.from_pretrained(
            self.get_model_path(), local_files_only = True)

    def get_task_str(self) -> str:
        return "sentiment-analysis"
