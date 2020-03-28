from typing import List, Dict

from .exceptions import (
    AlreadyRegisteredLevel,
    EntrypointDoesNotExist,
    EntrypointNotEmpty,
    LevelNotRegistered,
    MissingActionInsideLevel,
)

from sdk.level import Level as DevelopedLevel

from .types import LevelIdentifier, EntrypointCodename, ActionIdentifier


class Entrypoint:
    """Entrypoints base class to give entrance to levels
    """

    name = "Undefined"

    def __init__(
        self, level_identifier: LevelIdentifier, codename: EntrypointCodename
    ):
        self._level_identifier = level_identifier
        self._codename = codename
        self.__level = None

    @property
    def codename(self):
        return self._codename

    @property
    def level_identifier(self):
        return self._level_identifier

    def register(self, level: "Level"):
        """Register a Level in this entrypoint.

        The level registered will be the level started when the Entrypoint gets
        activated.

        :param: level: The level that will get registered in this entrypoint
        :type: level: Level
        """
        if self.__level is not None:
            raise EntrypointNotEmpty(
                "This entrypoint has already a Level registered"
            )
        self.__level = level

    def has_level(self):
        """Returns True if the Entrypoint has already a Level registered"""
        return self.__level is not None

    def __str__(self):
        return f"<Entrypoint name={self.name}>"


class Level:
    """Base class for the levels of the game
    """

    def __init__(
        self,
        identifier: LevelIdentifier,
        startpoint: Entrypoint,
        level: DevelopedLevel,
    ):
        self._identifier: LevelIdentifier = identifier
        self._startpoint: Entrypoint = startpoint
        self._entrypoints: List[Entrypoint] = []
        self._level: DevelopedLevel = level

    @property
    def startpoint(self) -> str:
        return self._startpoint

    @property
    def identifier(self) -> str:
        return self._identifier

    def get_entrypoint(self, codename: EntrypointCodename):
        for entrypoint in self._entrypoints:
            if entrypoint.codename == codename:
                return entrypoint

        raise EntrypointDoesNotExist

    def add_entrypoint(self, codename: EntrypointCodename):
        """Add an entrypoint to the level with the provided codename.

        If the codename exists already, don't do nothing.
        """
        try:
            self.get_entrypoint(codename)

        except EntrypointDoesNotExist:
            self._entrypoints.append(
                Entrypoint(
                    LevelIdentifier(self._identifier),
                    EntrypointCodename(codename),
                )
            )

    def get_action(self, action_identifier: ActionIdentifier) -> callable:
        action = self._level.api().get(action_identifier)
        if action is None:
            raise MissingActionInsideLevel(action_identifier)
        return action

    def __str__(self):
        return f"<Level id={self.identifier}>"


class Story:
    def __init__(self):
        self._levels: Dict[LevelIdentifier, Level] = {}

        # Level 0. Empty level needed to hook the first level in it
        level = Level(
            LevelIdentifier("origin"),
            Entrypoint("origin", "."),  # Dummy Startpoint
            DummyLevel(),
        )
        level.add_entrypoint("origin")
        self._levels["origin"] = level

    def _get_entrypoint(self, entrypoint: Entrypoint):
        """Returns the entrypoint in the story if exists.
        """

        level_associated = self._levels.get(entrypoint.level_identifier)
        if level_associated:
            registered_entrypoint = level_associated.get_entrypoint(
                entrypoint.codename
            )
            if registered_entrypoint:
                return registered_entrypoint

        raise EntrypointDoesNotExist

    def add_level(self, level: Level):

        # Check that the entrypoint of the startpoint exists
        level_entry = self._get_entrypoint(level.startpoint)

        # Search for previous registered levels with the same identifier
        if level.identifier in self._levels:
            raise AlreadyRegisteredLevel(
                f"The level {level.identifier} has been already registered in"
                "this history"
            )

        # Add the level
        self._levels[level.identifier] = level

        # Register the level into the startpoint
        level_entry.register(level)

    def resolve_action(
        self,
        level_identifier: LevelIdentifier,
        action_identifier: ActionIdentifier,
    ):
        level = self._levels.get(level_identifier)
        if level is None:
            raise LevelNotRegistered

        return level.get_action(action_identifier)


class DummyLevel(DevelopedLevel):
    def api(self):
        return {}
