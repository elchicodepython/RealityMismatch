class AlreadyRegisteredLevel(Exception):
    """Exception to be raised when a Level identifier collision appears
    in history at register time"""

    pass


class EntrypointDoesNotExist(Exception):
    """Exception to be raised when a queried entrypoint does not exist in
    story"""

    pass


class EntrypointNotEmpty(Exception):
    """Exception to be raised when a Level try to be registered
    in a Entrypoint which has already a registered level"""

    pass


class LevelNotRegistered(Exception):
    """Exception to be raised when a Story try to get access to a
    level not registered in it"""


class InvalidLevelStructure(Exception):
    """Exception to be raised when a folder is located inside
    levels folder with an invalid structure"""

    pass


class InvalidManifestStructure(Exception):
    """Exception to be raised when the Manifest for a Level
    does'nt have a valid structure"""

    pass


class DuplicatedLevelIdentifier(Exception):
    """Exception to be raised when two levels have the same level
    identifier even if they are not in use at the same time"""

    pass


class MissingStartpoint(Exception):
    """Exception to be raised when a Level uses a startpoint that
    its not available"""
    pass

class MissingCurrentClass(Exception):
    """Exception to be raised when a Level module does'nt have
    a Current object"""
    pass

class InvalidCurrentClass(Exception):
    """Exception to be raised when a Level does'nt inherits from
    sdk.level.Level abstract class"""
    pass

class MissingActionInsideLevel(Exception):
    """Exception to be raised when a Level tries to access to an
    action which does'nt exists"""
    pass