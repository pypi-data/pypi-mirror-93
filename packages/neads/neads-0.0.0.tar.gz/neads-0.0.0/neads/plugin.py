"""Module providing Plugin, ie. an object representation of a plugin."""

# TODO: really hate direct access to plugin method
#  I really feel that there should be some kind of abstraction

import importlib
import sys
from pathlib import Path


class Plugin:
    """Object representation of plugin."""

    def __init__(self, plugin_filename: Path):
        """Initialize a Plugin object.

        Parameters
        ----------
        plugin_filename
            Name of file, where the code of the plugin is.
        """

        plugin_module = self._import_module(plugin_filename)
        self.name = plugin_filename.stem
        self.version = getattr(plugin_module, 'PLUGIN_VERSION')
        self.method = getattr(plugin_module, 'method')

    def _import_module(self, module_filename):
        """Return Module object with the given path.

        Parameters
        ----------
        module_filename
            Path to module.

        Returns
        -------
        Module
            Module with the given path.
        """

        sys.path.append(str(module_filename.parents[0]))
        # TODO: the str conversion can be probably removed
        module = importlib.import_module(str(module_filename.stem))
        sys.path.pop()
        return module
