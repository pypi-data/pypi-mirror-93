from .error_handler import NeadsError


class NeadsInvalidProjectError(NeadsError):
    pass


class NeadsInvalidProjectDirectoryError(NeadsError):
    pass


class NeadsProjectIsNotOpen(NeadsError):
    pass
