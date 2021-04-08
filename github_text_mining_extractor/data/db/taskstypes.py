from enum import Enum

class TaskTypes(Enum):
    """ Enumeration with task types
    """
    Queued = 0
    InProgress = 1
    Done = 2
    Canceled = 3