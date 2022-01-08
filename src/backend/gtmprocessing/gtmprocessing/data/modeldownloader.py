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

""" Model Downloader Module
"""

from pathlib import Path
from typing import List

from transformers import pipeline  # type: ignore
from transformers.pipelines.base import Pipeline  # type: ignore


class ModelDownloader():
    """ Class in charge of downloading HuggingFace models.
    """

    __model_path: Path = Path("gtmprocessing/data/models/").absolute()

    @staticmethod
    def get_zsc() -> Pipeline:
        """ Downloads the Zero-Shot Classification model to
            gtmprocessing/data/models/zero_shot_classification.

        Returns:
            Pipeline: The Zero-Shot Classification model pipeline.
        """
        filepath: Path = ModelDownloader.__model_path / "zero_shot_classification"
        if not filepath.exists():
            print("Downloading Zero-Shot-Classification model. \
                Please don't shutdown the container.")
            zsc_pipeline: Pipeline = pipeline(
                "zero-shot-classification", model="facebook/bart-large-mnli")
            return zsc_pipeline.save_pretrained(str(filepath))
        return pipeline(
            task="zero-shot-classification", model=str(filepath), tokenizer=str(filepath))

    @staticmethod
    def get_sa() -> Pipeline:
        """ Downloads the Sentiment Analysis model to gtmprocessing/data/models/sentiment_analysis.

        Returns:
            Pipeline: The Sentiment Analysis model pipeline.
        """
        filepath: Path = ModelDownloader.__model_path / "sentiment_analysis"
        if not filepath.exists():
            print("Downloading Sentiment Analysis model. \
                  Please don't shutdown the container.")
            sa_pipeline: Pipeline = pipeline(
                "sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
            return sa_pipeline.save_pretrained(str(filepath))
        return pipeline(
            task="sentiment-analysis", model=str(filepath), tokenizer=str(filepath))

    @staticmethod
    def get_summ() -> Pipeline:
        """ Downloads the Summarization model to gtmprocessing/data/models/summarization.

        Returns:
            Pipeline: The Summarization model pipeline.
        """
        filepath: Path = ModelDownloader.__model_path / "summarization"
        if not filepath.exists():
            print("Downloading Summarization model. \
                  Please don't shutdown the container.")
            summ_pipeline: Pipeline = pipeline(
                "summarization", model="sshleifer/distilbart-cnn-12-6")
            return summ_pipeline.save_pretrained(str(filepath))
        return pipeline(
            task="summarization", model=str(filepath), tokenizer=str(filepath))


if __name__ == "__main__":

    zsc: Pipeline = ModelDownloader.get_zsc()

    sequence: str = "Hola, ¿qué tal?"
    labels: List[str] = ["Saludo", "Despedida", "Bienvenida"]

    print("ZSC: ", zsc(sequence, labels, multi_label=True))

    sa: Pipeline = ModelDownloader.get_sa()

    sequence_2: str = "I love you so much!"

    print("SA: ", sa(sequence_2))

    summ: Pipeline = ModelDownloader.get_summ()

    # pylint: disable=line-too-long
    article: str = """New York (CNN)When Liana Barrientos was 23 years old, she got married in Westchester County, New York.
    A year later, she got married again in Westchester County, but to a different man and without divorcing her first husband.
    Only 18 days after that marriage, she got hitched yet again. Then, Barrientos declared "I do" five more times, sometimes only within two weeks of each other.
    In 2010, she married once more, this time in the Bronx. In an application for a marriage license, she stated it was her "first and only" marriage.
    Barrientos, now 39, is facing two criminal counts of "offering a false instrument for filing in the first degree," referring to her false statements on the 2010 marriage license application, according to court documents.
    Prosecutors said the marriages were part of an immigration scam.
    On Friday, she pleaded not guilty at State Supreme Court in the Bronx, according to her attorney, Christopher Wright, who declined to comment further.
    After leaving court, Barrientos was arrested and charged with theft of service and criminal trespass for allegedly sneaking into the New York subway through an emergency exit, said Detective Annette Markowski, a police spokeswoman. In total, Barrientos has been married 10 times, with nine of her marriages occurring between 1999 and 2002.
    All occurred either in Westchester County, Long Island, New Jersey or the Bronx. She is believed to still be married to four men, and at one time, she was married to eight men at once, prosecutors say.
    Prosecutors said the immigration scam involved some of her husbands, who filed for permanent residence status shortly after the marriages.
    Any divorces happened only after such filings were approved. It was unclear whether any of the men will be prosecuted.
    The case was referred to the Bronx District Attorney\'s Office by Immigration and Customs Enforcement and the Department of Homeland Security Investigation Division. Seven of the men are from so-called "red-flagged" countries, including Egypt, Turkey, Georgia, Pakistan and Mali.
    Her eighth husband, Rashid Rajput, was deported in 2006 to his native Pakistan after an investigation by the Joint Terrorism Task Force.
    If convicted, Barrientos faces up to four years in prison.  Her next court appearance is scheduled for May 18.
    """

    print("SUMM: ", summ(article, max_length=150, min_length=50, do_sample=False))
