from os import listdir
from os import path
import json

from .game import Level, Entrypoint
from .types import LevelIdentifier, EntrypointCodename
from .exceptions import (
    InvalidLevelStructure,
    InvalidManifestStructure,
    DuplicatedLevelIdentifier,
)


class Loader:
    # TODO: Doc this class

    LEVELS_PATH = "backend/levels"
    MINIMUM_LEVEL_FILES = ("manifest.json", "level.py")
    MINIMUM_MANIFEST_KEYS = ("id", "startpointLevelId", "startpointCodename")

    @classmethod
    def local_levels(cls):

        ids_parsed = []

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
                raise InvalidManifestStructure
