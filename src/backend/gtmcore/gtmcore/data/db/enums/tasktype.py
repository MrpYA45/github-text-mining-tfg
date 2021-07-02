""" Task Type enum module
"""

from enum import Enum


class TaskType(Enum):
    """ Enumeration with the types of the tasks.
    """
    ZSC = 0
    SA = 1
    SUMM = 2
    NOT_SET = -1
