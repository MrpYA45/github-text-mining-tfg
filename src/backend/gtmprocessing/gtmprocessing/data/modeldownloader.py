from pathlib import Path
from typing import List

from transformers import pipeline  # type: ignore
from transformers.pipelines.base import Pipeline  # type: ignore


class ModelDownloader():

    __model_path: Path = Path("gtmprocessing/data/models/").absolute()

    @staticmethod
    def get_zsc() -> Pipeline:
        filepath: str = ModelDownloader.__model_path / "zero_shot_classification"
        zsc_pipeline: Pipeline = pipeline("zero-shot-classification",
                                          model="facebook/bart-large-mnli")
        zsc_pipeline.save_pretrained(filepath)
        return zsc_pipeline

    @ staticmethod
    def get_sa() -> Pipeline:
        filepath: str = ModelDownloader.__model_path / "sentiment_analysis"
        sa_pipeline: Pipeline = pipeline(
            "sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
        sa_pipeline.save_pretrained(filepath)
        return sa_pipeline

    @ staticmethod
    def get_summ() -> Pipeline:
        filepath: str = ModelDownloader.__model_path / "summarization"
        summ_pipeline: Pipeline = pipeline(
            "summarization", model="sshleifer/distilbart-cnn-12-6")
        summ_pipeline.save_pretrained(filepath)
        return summ_pipeline


if __name__ == "__main__":

    zsc: Pipeline = ModelDownloader.get_zsc()

    sequence: str = "Hola, ¿qué tal?"
    labels: List[str] = ["Saludo", "Despedida", "Bienvenida"]

    print("ZSC: ", zsc(sequence, labels, multi_label=True))

    sa: Pipeline = ModelDownloader.get_sa()

    sequence = "I love you so much!"

    print("SA: ", sa(sequence))

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
