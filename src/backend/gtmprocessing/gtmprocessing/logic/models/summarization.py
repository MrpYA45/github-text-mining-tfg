from typing import List

from gtmprocessing.data.modeldownloader import ModelDownloader
from gtmprocessing.logic.models.basemodel import BaseModel
from transformers.pipelines.base import Pipeline  # type: ignore


class Summarization(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.__pipeline: Pipeline = self.get_pipeline()

    def get_pipeline(self) -> Pipeline:
        try:
            return super().get_pipeline()
        except KeyError:
            return ModelDownloader.get_summ()

    def apply(self, data: dict):
        sequences: List[str] = data["sequences"]
        results: List[dict] = []
        for sequence in sequences:
            results.append(self.__pipeline(sequence, multi_label=True))
        return results

    def get_method_str(self) -> str:
        return "summarization"
