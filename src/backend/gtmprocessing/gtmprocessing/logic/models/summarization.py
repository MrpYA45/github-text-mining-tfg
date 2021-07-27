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

from gtmprocessing.logic.models.basemodel import BaseModel
from gtmprocessing.logic.utils.textpreprocessor import \
    TextPreprocessor  # type: ignore
from transformers.pipelines.base import Pipeline


class Summarization(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.__pipeline: Pipeline = self.get_pipeline()

    def apply(self, data: dict) -> dict:
        max_length: int = data.get("max_length")
        min_length: int = data.get("min_length")
        texts: List[str] = data.get("texts")

        preprocessor = TextPreprocessor(self.__pipeline.tokenizer)

        sentences: List[str] = []
        
        for text in texts:
            sentences += preprocessor.preprocess([text])

        final_summarized_text: str = ""

        start_time: float = time.time()

        for sentence in sentences:
            summarized_text = self.__pipeline(
                sentence,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            ).get("summary_text", "")
            final_summarized_text += (" ", summarized_text)

        exec_time: float = time.time() - start_time

        outcome_data: dict = {
            "summarized_text": summarized_text
        }

        return outcome_data, exec_time

    def get_model_str(self) -> str:
        return "summarization"
