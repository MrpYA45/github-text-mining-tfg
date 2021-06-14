from abc import ABC, abstractmethod

from transformers import pipeline


class BaseAlgorithm(ABC):

    def __init__(self) -> None:
        self.__pipeline = None
        self.__raw_data = None
        self.__processed_data = None
        self.__base_path = "./app/backend/gtmprocessing/gtmprocessing/data/models"

    def get_base_path(self):
        return self.__base_path

    def set_raw_data(self, data) -> None:
        self.__raw_data = data

    def get_processed_data(self):
        print(self.__processed_data)

    @staticmethod
    def get_method_str() -> str:
        return None

    @abstractmethod
    def get_pipeline(self) -> pipeline:
        return None

    @abstractmethod
    def apply(self, data: dict):
        return None
