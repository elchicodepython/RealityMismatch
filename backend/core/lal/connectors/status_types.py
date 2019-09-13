from enum import Enum


class Status(Enum):
    """Enumeration of available Connection statuses returned
    by laboratory connectors.
    """
    INITIALIZATION_IN_PROGRESS = 0
    NO_WORKERS_AVAILABLE = 1
    LAB_INITIALIZED = 2
    CLOSING_LAB = 3
    LAB_CLOSED = 4
