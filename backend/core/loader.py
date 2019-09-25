from os import listdir
from os import path, mkdir
import json
import shutil

import tarfile
from typing import List

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
    LEVELS_UI = "ui/src/levels"
    TEMP = '/tmp'
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
    def install_new_level(self, level_filename: str):
        """Load a Level from a .tar.gz file.

        Raises a FileNotFoundError if the level_filename provided does'nt exist
        Raises a InvalidManifestStructure if the manifest is invalid.

        :param level_filename: .tar.gz file with the level structure
        :type level_filename: str
        """

        assert level_filename.endswith('.level'), ('The provided file is not '
                                                   'a valid level')

        level_name = path.basename(level_filename).split('.')[0]

        with tarfile.open(level_filename, 'r:gz') as level_tar:
            level_tar.extractall(path=path.join(self.TEMP, level_name))

        level_tmp_folder = path.join(self.TEMP, level_name)

        manifest_file = path.join(level_tmp_folder, 'manifest.json')

        with open(manifest_file) as manifest:
            level_manifest = json.loads(manifest.read())

        self.check_valid_level_manifest(level_manifest)

        level_backend_path = path.join(self.LEVELS_PATH, level_manifest['id'])
        level_frontend_path = path.join(self.LEVELS_UI, level_manifest['id'])

        # TODO check not in local levels

        # Create backend structure
        mkdir(level_backend_path)

        # Create frontend structure
        mkdir(level_frontend_path)

        # Move files into level folder
        shutil.move(manifest_file, level_backend_path)
        self.__move_to(path.join(level_tmp_folder, 'backend'),
                       level_backend_path)

        self.__move_to(path.join(level_tmp_folder, 'frontend'),
                       level_frontend_path)

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
            # If exists, add to levels, remove from local_levels
            if local_level.startpoint.level_identifier == level.identifier:
                levels.append(local_levels.pop(idx))

        # Raise for unregistered levels
        if local_levels:
            missing_startpoints = ', '.join([
                level.startpoint.level_identifier for level in local_levels
            ])
            raise MissingStartpoint(missing_startpoints)

        # Return ordered levels

        return levels
