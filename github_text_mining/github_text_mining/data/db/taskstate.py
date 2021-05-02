""" Task State enum module
"""

from enum import Enum


class TaskState(Enum):
    """ Enumeration with the states of the tasks.
    """
    Queued = 0
    CapturingData = 1
    Waiting = 2
    InProgress = 3
    Done = 4
    OutDated = -1
