""" Task State enum module
"""

from enum import Enum


class TaskState(Enum):
    """ Enumeration with the states of the tasks.
    """
    QUEUED = 0
    CAPTURING_DATA = 1
    WAITING = 2
    IN_PROGRESS = 3
    DONE = 4
    OUTDATED = -1
