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
from typing import Any, Dict, List

from gtmcore.data.db.results.comment import Comment
from gtmcore.data.db.results.issue import Issue
from gtmcore.logic.dbmanager import DBManager
from gtmprocessing.logic.models.basemodel import BaseModel
from transformers.pipelines.base import Pipeline  # type: ignore


class Summarization(BaseModel):

    def __init__(self, dbmanager: DBManager) -> None:
        super().__init__()
        self.__dbmanager: DBManager = dbmanager
        self.__pipeline: Pipeline = self.get_pipeline()

        self.__with_comments: bool = False
        self.__max_length: int = 0
        self.__min_length: int = 0

    def set_params(self, params: Dict[str, Any]) -> None:
        super().set_params(params)

        self.__with_comments = bool(params.get("with_comments", False))
        self.__max_length = int(params.get("max_length", 150))
        self.__min_length = int(params.get("min_length", 50))

    def preprocess(self) -> None:
        try:
            issue: Issue = self.__dbmanager.get_issue(
                self._repo_dir, self._issue_id)

            inputs: List[str] = [issue.description]

            if self.__with_comments:
                comments: List[Comment] = self.__dbmanager.get_comments(
                    self._repo_dir, self._issue_id)
                inputs += [comment.body for comment in comments]

            self._inputs = self.chunk_input(inputs, self.__pipeline.tokenizer)
        except ValueError as err:
            raise ValueError("Missing, incorrect or damaged model paramethers.") from err

    def apply(self) -> None:

        start_time: float = time.time()

        summarized_inputs: str = ""

        for text in self._inputs:
            max_length = len(text) if self.__max_length > len(text) else self.__max_length
            min_length = 0 if self.__min_length > len(text) else self.__min_length
            summarized_input = self.__pipeline(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )[0].get("summary_text", "")
            summarized_inputs += (" " + summarized_input)

        self._exec_time = time.time() - start_time

        self._outcome = {
            "input_chunks": self._inputs,
            "summarized_text": summarized_inputs
        }

    def get_model_str(self) -> str:
        return "summarization"
