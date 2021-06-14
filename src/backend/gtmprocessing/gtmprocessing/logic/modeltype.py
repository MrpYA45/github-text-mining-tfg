""" Model Type enum module
"""

from enum import Enum


class ModelType(Enum):
    """ Enumeration with the types of models.
    """
    ZERO_SHOT_CLASSIFIER = 0
    SENTIMENTS_ANALYSIS = 1
    SUMMARIZATION = 2
