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

""" Base Model class module.
"""
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from transformers import pipeline  # type: ignore
from transformers.pipelines.base import Pipeline  # type: ignore
from transformers.tokenization_utils import PreTrainedTokenizer  # type: ignore
from gtmcore.logic.utils.datautils import DataUtils
from gtmprocessing.logic.utils.textpreprocessor import TextPreprocessor


class BaseModel(ABC):
    """ Abstract base class used for NLP model classes.
    """

    _base_path = Path("gtmprocessing/data/models").absolute()

    def __init__(self) -> None:
        self._repo_dir: str = ""
        self._issue_id: int = -1
        self._inputs: List[str] = []
        self._outcome: Dict[str, Union[str,
                                       float, List[str], List[float]]] = {}
        self._exec_time: float = 0.0

    def get_pipeline(self) -> Pipeline:
        """ Gets the model pipeline.

        Returns:
            Pipeline: the model pipeline.
        """
        return pipeline(
            task=self.get_model_str(),
            model=self.get_model_path(),
            tokenizer=self.get_model_path()
        )

    @classmethod
    def chunk_input(cls,
                    raw_inputs: List[str],
                    tokenizer: Optional[PreTrainedTokenizer]) -> List[str]:
        """ Breaks inputs into smaller fragments according to the maximum size
            accepted by the tokenizer of the model.

        Args:
            raw_inputs (List[str]): The list of inputs.
            tokenizer (Optional[PreTrainedTokenizer]): The model tokenizer.

        Returns:
            List[str]: List of fragments of the entries.
        """

        # Creates a text preprocessor instance with the tokenizer.
        preprocessor: TextPreprocessor = TextPreprocessor(tokenizer)

        # List with the sectionated inputs in paragraphs adjusted to the tokenizer limits.
        sliced_inputs: List[str] = []

        # For each single raw input (piece of text).
        for raw_input in raw_inputs:

            # raw_input empty strings are skipped.
            if not "".join(raw_input.split()):
                continue

            logging.debug("CHUNKING: %s", str(raw_input))

            # The sentences that compose each paragraph are checked.
            sentences: List[str] = DataUtils.split_text_into_sentences(
                raw_input)

            logging.debug("SENTENCES: %s", str(sentences))

            # Phrases are grouped into sections according to the tokenizer limits.
            sections: List[List[str]] = preprocessor.preprocess(sentences)

            logging.debug("SECTIONS: %s", str(sections))

            # The sentences of each section are joined together to form new paragraphs.
            sliced_inputs += [" ".join(section) for section in sections]

        return sliced_inputs

    def get_model_path(self) -> str:
        """ Gets the path where the model is stored.

        Returns:
            str: The path to the model.
        """
        model_folder: str = self.get_model_str().replace("-", "_")
        return str(self._base_path / model_folder)

    def set_params(self, params: Dict[str, Any]) -> None:
        """ Sets the parameters needed to run the model pipeline.
        """
        self._repo_dir = str(params.get("repo_dir", ""))
        self._issue_id = int(params.get("issue_id", -1))

    def get_outcome(self) -> Tuple[Dict[str, Any], float]:
        """ Gets the outcome and the execution time of the model pipeline.

        Returns:
            Tuple[Dict[str, Any], float]: Tuple with the outcome data and the execution time.
        """
        return (self._outcome, self._exec_time)

    @abstractmethod
    def preprocess(self) -> None:
        """ Calculate the model inputs from the experiment parameters.
        """

    @abstractmethod
    def apply(self) -> None:
        """ Apply the model pipeline to the inputs using the experiment parameters.
        """

    @abstractmethod
    def get_model_str(self) -> str:
        """ Gets the model string.
        """
