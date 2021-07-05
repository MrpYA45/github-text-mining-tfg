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
            task=str(self.get_method_str()),
            model=str(self.get_base_path().joinpath(self.get_method_str())),
            tokenizer=str(self.get_base_path().joinpath(self.get_method_str())))

    @abstractmethod
    def apply(self, data: dict) -> None:
        return None

    @abstractmethod
    def get_method_str(self) -> str:
        return ""
