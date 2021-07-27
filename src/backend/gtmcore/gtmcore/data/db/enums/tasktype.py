""" Task Type enum module
"""

from enum import Enum


class TaskType(Enum):
    """ Enumeration with the types of the tasks.
    """
    EXTRACTION = 0
    PROCESSING = 1
