from .error_handler import NeadsException


class NeadsDatabaseException(NeadsException):
    pass


class NeadsDatabaseError(NeadsException):
    pass


class DataNotFound(NeadsDatabaseException):
    pass


class NeadsDatabaseIsNotOpen(NeadsDatabaseError):
    pass
