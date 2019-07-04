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
