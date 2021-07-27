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
from abc import ABC, abstractmethod
from pathlib import Path

from transformers import pipeline  # type: ignore
from transformers.pipelines.base import Pipeline  # type: ignore


class BaseModel(ABC):

    def __init__(self) -> None:
        self.__pipeline = None
        self.__raw_data = None
        self.__processed_data = None
        self.__base_path = Path("gtmprocessing/data/models").absolute()

    def get_base_path(self):
        return self.__base_path

    def set_raw_data(self, data) -> None:
        self.__raw_data = data

    def get_processed_data(self):
        print(self.__processed_data)

    def get_pipeline(self) -> Pipeline:
        return pipeline(
            task=str(self.get_model_str().replace("_", "-")),
            model=str(self.get_base_path().joinpath(self.get_model_str())),
            tokenizer=str(self.get_base_path().joinpath(self.get_model_str())))

    @abstractmethod
    def apply(self, data: dict) -> list:
        return []

    @abstractmethod
    def get_model_str(self) -> str:
        return ""
