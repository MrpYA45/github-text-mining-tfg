from typing import List

from gtmprocessing.logic.algorithms.basealgorithm import BaseAlgorithm
from transformers import pipeline


class ZeroShotClassifier(BaseAlgorithm):

    def __init__(self) -> None:
        super().__init__()
        self.__pipeline = self.get_pipeline()

    def get_pipeline(self) -> pipeline:
        return pipeline(task="zero-shot-classification",
                        model=self.get_base_path() + "/zero_shot_classification",
                        tokenizer=self.get_base_path() + "/zero_shot_classification")

    def apply(self, data: dict):
        labels: List[str] = data["labels"]
        sequences: List[str] = data["sequences"]
        results: List[dict] = []
        for sequence in sequences:
            results.append(self.__pipeline(sequence, labels, multi_label=True))
        return results
