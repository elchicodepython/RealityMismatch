from os import listdir
from os import path
from typing import List
import json

from .game import Level, Entrypoint
from .types import LevelIdentifier, EntrypointCodename
from .exceptions import (
    InvalidLevelStructure,
    InvalidManifestStructure,
    DuplicatedLevelIdentifier,
    MissingStartpoint
)


class Loader:
    # TODO: Doc this class

    LEVELS_PATH = "backend/levels"
    MINIMUM_LEVEL_FILES = ("manifest.json", "level.py")
    MINIMUM_MANIFEST_KEYS = ("id", "startpointLevelId", "startpointCodename", "entrypoints")

    @classmethod
    def local_levels(cls):
        """Return a generator object with instances of Levels
        found in levels folder"""

        ids_parsed: List[LevelIdentifier] = []

        possible_levels = listdir(cls.LEVELS_PATH)
        for level in possible_levels:
            level_folder = listdir(path.join(cls.LEVELS_PATH), level)
            for needed_file in cls.MINIMUM_LEVEL_FILES:
                if needed_file not in level_folder:
                    raise InvalidLevelStructure

            level_manifest = json.loads(
                path.join(path.join(cls.LEVELS_PATH, level), "manifest.json")
            )
            cls.check_valid_level_manifest(level_manifest)

            if level_manifest["id"] in ids_parsed:
                raise DuplicatedLevelIdentifier

            level = Level(
                LevelIdentifier(level_manifest["id"]),
                Entrypoint(
                    LevelIdentifier(level_manifest["startpointLevelId"]),
                    EntrypointCodename(level_manifest["startpointCodename"]),
                ),
            )
            ids_parsed.append(level_manifest["id"])
            yield level

    @classmethod
    def check_valid_level_manifest(cls, level_manifest: dict):
        """Checks that the JSON structure for a manifest has all
        the needed keys, raises InvalidManifestStructure otherwise.

        :param level_manifest: Manifest to check
        :type level_manifest: dict
        """

        for key in cls.MINIMUM_MANIFEST_KEYS:
            if key not in level_manifest:
                raise InvalidManifestStructure(f'Missing Key {key}')

    @classmethod
    def order_levels(cls):
        levels: List[Level] = []

        local_levels = list(cls.local_levels())

        # Search for origin story
        for idx, level in enumerate(local_levels):
            if level.startpointCodename == 'origin' and level.startpointLevelId == 'origin':
                levels[0] = local_levels.pop(idx)

        # For each entrypoint of the level
        
        for idx, local_level in enumerate(local_levels):
            if local_level.startpoint.level_identifier == level.identifier:
                levels.append(local_levels.pop(idx))

        # If exists, add to levels, remove from local_levels

        # Raise for unregistered levels
        if local_levels:
            missing_startpoints = ', '.join([
                level.startpoint.level_identifier for level in local_levels
            ])
            raise MissingStartpoint(missing_startpoints)

        # Return ordered levels

        return levels