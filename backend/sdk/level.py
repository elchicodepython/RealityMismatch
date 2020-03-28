from abc import ABCMeta, abstractmethod

from typing import Dict, Callable

from core.types import ActionIdentifier


class LevelView(metaclass=ABCMeta):
    @abstractmethod
    def action(self, *args, **kwargs):
        pass


class Level(metaclass=ABCMeta):
    @abstractmethod
    def api(self) -> Dict[ActionIdentifier, Callable]:
        pass
