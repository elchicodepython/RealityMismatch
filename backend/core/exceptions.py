
class AlreadyRegisteredLevel(Exception):
    """Exception to be raised when a Level identifier collision appears
    in history at register time"""
    pass


class EntrypointDoesNotExist(Exception):
    """Exception to be raised when a queried entrypoint does not exist in
    history"""
    pass
