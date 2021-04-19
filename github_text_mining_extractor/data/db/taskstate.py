""" Task State enum module
"""

from enum import Enum


class TaskState(Enum):
    """ Enumeration with the states of the tasks.
    """
    Queued = 0
    CapturingData = 1
    InProgress = 2
    Done = 3
    OutDated = 4
