import logging
from typing import List

from gtmprocessing.data.modeldownloader import ModelDownloader
from gtmprocessing.logic.models.basemodel import BaseModel
from transformers.pipelines.base import Pipeline  # type: ignore


class ZeroShotClassifier(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.__pipeline: Pipeline = self.get_pipeline()

    def get_pipeline(self) -> Pipeline:
        try:
            return super().get_pipeline()
        except KeyError:
            return ModelDownloader.get_zsc()

    def apply(self, data: dict) -> None:
        labels: List[str] = data["labels"]
        sequences: List[str] = data["sequences"]
        results: List[dict] = []
        logging.debug("[GTMProcessing] LABELS: %s", str(labels))
        for sequence in sequences:
            logging.debug("[GTMProcessing] SEQUENCE: %s", sequence)
            results.append(self.__pipeline(sequence, labels, multi_label=True))
        return results

    def get_method_str(self) -> str:
        return "zero-shot-classification"
