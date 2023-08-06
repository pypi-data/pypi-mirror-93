from .error_handler import NeadsError


class NeadsPluginPoolError(NeadsError):
    pass


class NeadsPluginPoolIsNotOpen(NeadsPluginPoolError):
    pass


class NeadsPluginNotFound(NeadsPluginPoolError):
    pass
