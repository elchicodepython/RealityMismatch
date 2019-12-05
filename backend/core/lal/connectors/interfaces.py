from abc import ABC, abstractmethod

from . import Status


class AccessInformation(ABC):
    """Information needed to access to a Lab by a client"""

    pass


class Connection(ABC):
    @abstractmethod
    def open(self) -> bool:
        """Initializes a connection with a Lab provider.
        Return True if no errors are provided.
        """
        pass

    @abstractmethod
    def status(self) -> Status:
        """Return the lab status.
       eg: Status.LAB_INITIALIZED"""
        pass

    @abstractmethod
    def close(self):
        """TearDown the laboratory."""
        pass
