""" Task State enum module
"""

from enum import Enum


class TaskState(Enum):
    """ Enumeration with the states of the tasks.
    """
    QUEUED = 0
    IN_PROGRESS = 1
    DONE = 2
    OUTDATED = -1
