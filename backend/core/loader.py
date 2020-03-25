from os import listdir
from os import path, mkdir
from importlib import import_module
import json
import shutil

import tarfile
from typing import List

from bridge.config import conf
from sdk.level import Level as DevelopedLevel
from .game import Level, Entrypoint
from .types import LevelIdentifier, EntrypointCodename
from .exceptions import (
    AlreadyRegisteredLevel,
    InvalidLevelStructure,
    InvalidManifestStructure,
    DuplicatedLevelIdentifier,
    MissingStartpoint,
    MissingCurrentClass,
    InvalidCurrentClass,
)


class Loader:
    """Provides functionality for loading, installing and ordering levels.
    """

    LEVELS_PATH = conf["LEVELS_PATH"]
    LEVELS_UI = conf["LEVELS_UI"]
    TEMP = conf["TMP_FILES"]
    MINIMUM_LEVEL_FILES = ("manifest.json", "level.py")
    MINIMUM_MANIFEST_KEYS = (
        "id",
        "startpointLevelId",
        "startpointCodename",
        "entrypoints",
    )

    @classmethod
    def local_levels(cls):
        """Return a generator object with instances of Levels
        found in levels folder"""

        ids_parsed: List[LevelIdentifier] = []

        possible_levels = listdir(cls.LEVELS_PATH)
        for level in possible_levels:
            level_folder = listdir(path.join(cls.LEVELS_PATH, level))
            for needed_file in cls.MINIMUM_LEVEL_FILES:
                if needed_file not in level_folder:
                    raise InvalidLevelStructure

            with open(
                path.join(path.join(cls.LEVELS_PATH, level), "manifest.json")
            ) as level_manifest_file:
                level_manifest_data = level_manifest_file.read()

            level_manifest = json.loads(level_manifest_data)
            cls.check_valid_level_manifest(level_manifest)

            if level_manifest["id"] in ids_parsed:
                raise DuplicatedLevelIdentifier

            level_module = import_module(f"levels.{level}.level")
            level_class = getattr(level_module, "Current")

            if not level_class:
                raise MissingCurrentClass(
                    "Level module should provide a `Current` class"
                )

            try:
                if not issubclass(level_class, DevelopedLevel):
                    raise TypeError
            except TypeError:
                raise InvalidCurrentClass(
                    "Current class should inherit from sdk.level.Level"
                )

            level_instance = level_class()

            new_level = Level(
                LevelIdentifier(level_manifest["id"]),
                Entrypoint(
                    LevelIdentifier(level_manifest["startpointLevelId"]),
                    EntrypointCodename(level_manifest["startpointCodename"]),
                ),
                level_instance,
            )
            ids_parsed.append(level_manifest["id"])
            yield new_level

    def __move_to(origin_folder: str, dst_folder: str):
        """Move all the files and folders inside a origin to a destination.

        :param origin_folder: Folder with files and directories inside to move.
        :type origin_folder: str

        :param dst_folder: Folder to receive the moved files and directories.
        :type dst_folder: str
        """

        for file_or_folder in listdir(origin_folder):
            shutil.move(path.join(origin_folder, file_or_folder), dst_folder)

    @classmethod
    def _check_level_exists(cls, level_name: str):
        """Check if a level exists locally by searching it inside the installed
        levels"""

        return level_name in listdir(cls.LEVELS_PATH)

    @classmethod
    def install_new_level(self, level_filename: str):
        """Load a Level from a .lvl file.

        Raises FileNotFoundError if the level_filename provided does'nt exist
        Raises InvalidManifestStructure if the manifest is invalid.
        Raises AlreadyRegisteredLevel if there is a level with the same name
         already installed locally.

        :param level_filename: .lvl file with the level structure
        :type level_filename: str
        """

        assert level_filename.endswith(".lvl"), (
            "The provided file is not " "a valid level"
        )

        level_name = path.basename(level_filename).split(".")[0]

        with tarfile.open(level_filename, "r:gz") as level_tar:
            level_tar.extractall(path=path.join(self.TEMP, level_name))

        level_tmp_folder = path.join(self.TEMP, level_name)

        manifest_file = path.join(level_tmp_folder, "manifest.json")

        with open(manifest_file) as manifest:
            level_manifest = json.loads(manifest.read())

        self.check_valid_level_manifest(level_manifest)

        level_backend_path = path.join(self.LEVELS_PATH, level_manifest["id"])
        level_frontend_path = path.join(self.LEVELS_UI, level_manifest["id"])

        if not self._check_level_exists(level_name):
            raise AlreadyRegisteredLevel

        # Create backend structure
        mkdir(level_backend_path)

        # Create frontend structure
        mkdir(level_frontend_path)

        # Move files into level folder
        shutil.move(manifest_file, level_backend_path)
        self.__move_to(
            path.join(level_tmp_folder, "backend"), level_backend_path
        )

        self.__move_to(
            path.join(level_tmp_folder, "frontend"), level_frontend_path
        )

        # Remove temporary folder
        shutil.rmtree(level_tmp_folder)

    @classmethod
    def check_valid_level_manifest(cls, level_manifest: dict):
        """Checks that the JSON structure for a manifest has all
        the needed keys, raises InvalidManifestStructure otherwise.

        :param level_manifest: Manifest to check
        :type level_manifest: dict
        """

        for key in cls.MINIMUM_MANIFEST_KEYS:
            if key not in level_manifest:
                raise InvalidManifestStructure(f"Missing Key {key}")

    @classmethod
    def order_levels(cls):
        levels: List[Level] = []

        local_levels = list(cls.local_levels())

        # Search for origin story
        for idx, level in enumerate(local_levels):
            if (
                level.startpointCodename == "origin"
                and level.startpointLevelId == "origin"
            ):
                levels[0] = local_levels.pop(idx)

        # For each entrypoint of the level
        for idx, local_level in enumerate(local_levels):
            # If exists, add to levels, remove from local_levels
            if local_level.startpoint.level_identifier == level.identifier:
                levels.append(local_levels.pop(idx))

        # Raise for unregistered levels
        if local_levels:
            missing_startpoints = ", ".join(
                [level.startpoint.level_identifier for level in local_levels]
            )
            raise MissingStartpoint(missing_startpoints)

        # Return ordered levels

        return levels
