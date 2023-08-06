"""Module providing PluginPool managing plugins."""

# TODO: change open-close to enter-exit protocol
#  also fix it!

from pathlib import Path
import os
import glob
from abc import abstractmethod

from neads.plugin import Plugin
import neads.error_handlers.plugin_pool_error_handler as eh


class PluginPool:
    """Base class for plugin pools.

    Plugin pool stores plugins and provides access to their method.
    It is possible to view it as a database for plugins.

    Attributes
    ----------
    is_open : bool
        Says whether the PluginPool is open. That is, whether is ready
        for use. It is forbidden to ask for any plugin, when the
        PluginsPool is not open.
    """

    @staticmethod
    @abstractmethod
    def create_plugin_pool(main_dir):
        """Create a plugin pool layout in given directory.

        Parameters
        ----------
        main_dir
            Directory where the plugin pool should reside. It does not
            need to exist. However, if it does, it must be empty.
        """
        pass

    def __init__(self, main_dir: Path):
        """Initialize PluginPool object with given directory.

        It is assumed that there is a valid plugin pool in the given
        directory.

        Parameters
        ----------
        main_dir : Path
            Directory, where the PluginPool is located.
        """

        self.is_open = False

    def get_plugin(self, name: str, version: int) -> Plugin:
        """Return Plugin with given name and version, if it is present.

        Parameters
        ----------
        name : str
            Name of requested Plugin.
        version : int
            Version of requested Plugin.

        Returns
        -------
            Plugin with the given name and version.

        Raises
        ------
        NeadsPluginPoolIsNotOpen
            When the PluginPool is not open (was not called the method
            open).
        NeadsPluginNotFound
            When the plugin is not found in the pool.
        """

        if not self.is_open:
            raise eh.NeadsPluginPoolIsNotOpen('Plugin pool must be open '
                                              'when acquiring plugin')
        return self._get_plugin(name, version)

    @abstractmethod
    def _get_plugin(self, name: str, version: int) -> Plugin:
        """Actually return the plugin.

        The error handling is assumed to be done. This method depends
        entirely on the particular PluginPool type.

        Parameters
        ----------
        name : str
            Name of requested Plugin.
        version : int
            Version of requested Plugin.

        Returns
        -------
            Plugin with the given name and version.

        Raises
        ------
        NeadsPluginNotFound
            When the plugin is not found in the pool.
        """
        pass

    def open(self):
        """Prepare the PluginPool for use."""
        if self.is_open:
            raise eh.NeadsPluginPoolError('Plugin pool is already open.')
        self._open()
        self.is_open = True

    @abstractmethod
    def _open(self):
        """Prepare the PluginPool for use.

        The error handling is assumed to be done.
        """
        pass

    def close(self):
        """End an active state of the PluginPool."""
        if not self.is_open:
            raise eh.NeadsPluginPoolError('Plugin pool is not open.')
        self.is_open = False
        self._close()

    @abstractmethod
    def _close(self):
        """End an active state of the PluginPool.

        The error handling is assumed to be done.
        """
        pass


class SinglePluginPool(PluginPool):
    """Plugin pool which searches for plugins in a single directory."""

    @staticmethod
    def create_plugin_pool(main_dir):
        """Create a plugin pool layout in given directory.

        The default layout is plain, however, it is possible to
        customise it arbitrarily.

        Parameters
        ----------
        main_dir
            Directory where the plugin pool should reside. It does not
            need to exist. However, if it does, it must be empty.
        """

        # TODO: for some kind of complicated inner organization
        #  probably create directory for each plugin type
        if not os.path.exists(main_dir):
            os.mkdir(main_dir)

        if len(os.listdir(main_dir)) != 0:
            raise eh.NeadsPluginPoolError('The directory is not empty.')

    def __init__(self, main_dir: Path):
        """Initialize PluginPool object with given directory.
        
        It is assumed that there is a valid plugin pool in the given 
        directory.

        Parameters
        ----------
        main_dir
            Directory, where the PluginPool is located.
        """

        super().__init__(main_dir)
        self._main_dir = main_dir
        self._plugins = None

    def _get_plugin(self, name: str, version: int) -> Plugin:
        """Return Plugin with given name and version, if it is present.

        Parameters
        ----------
        name : str
            Name of requested Plugin.
        version : int
            Version of requested Plugin.

        Returns
        -------
            Plugin with the given name and version.

        Raises
        ------
        NeadsPluginNotFound
            When the plugin is not found in the pool.
        """

        try:
            return self._plugins[(name, version)]
        except KeyError as e:
            raise eh.NeadsPluginNotFound(f"Plugin '{name}' with version"
                                         f" {version} was not found.") \
                from e

    def _load_plugins(self) -> dict:
        """Load plugins and return their object versions in dictionary.

        Returns
        -------
        dict
            Dictionary with all found plugins. Key for a particular
            plugin is tuple (name, version).
        """

        regex = str(self._main_dir) + '\**\[!_]*.py'

        plugins = {}
        for filename in glob.iglob(regex, recursive=True):  # all .py files
            plugin = Plugin(Path(filename))
            plugins[(plugin.name, plugin.version)] = plugin
        return plugins

    def _open(self):
        """Prepare the PluginPool for use.

        Read plugins into memory.
        """

        self._plugins = self._load_plugins()

    def _close(self):
        """End an active state of the PluginPool.

        Releases the loaded plugins.
        """

        self._plugins = None


class CascadedPluginPool(PluginPool):
    """Plugin pool which chains together a cascade of SinglePluginPools."""

    _CENTRAL_POOLS = [
        Path(__file__).parents[1] / 'plugins'
    ]  # TODO: add central PP directory

    @staticmethod
    def create_plugin_pool(main_dir, *kwargs):
        """Create a plugin pool layout in given directories.

        Parameters
        ----------
        main_dir
            Directory where the plugin pool should reside. It does not
            need to exist. However, if it does, it must be empty.
        kwargs
            Other directories with the same meaning.
        """

        dirs = (main_dir, *kwargs)
        for d in dirs:
            SinglePluginPool.create_plugin_pool(d)

    def __init__(self, main_dir: Path, *kwargs,
                 link_to_central_pools: bool = True):
        """Initialize PluginPool object with given directory.

        It is assumed that there is a valid plugin pool in the given
        directories.

        The order of the directories matters. First it is searched for
        the plugin in the main_dir. If the plugin is not found,
        the search proceeds in the other directories by their order.

        Parameters
        ----------
        main_dir : Path
            Directory, where the PluginPool is located.
        kwargs : Iterable[Path]
            Other directories.
        link_to_central_pools : bool
            Whether to add link to central plugin pool(s) as well,
            ie. to their directories. The directories are stored in
            `_CENTRAL_POOLS` field.
        """

        super().__init__(main_dir)
        if link_to_central_pools:
            dirs = (main_dir, *kwargs, *self._CENTRAL_POOLS)
        else:
            dirs = (main_dir, *kwargs)
        self._pools = [SinglePluginPool(d) for d in dirs]

    def _get_plugin(self, name: str, version: int) -> Plugin:
        """Return Plugin with given name and version, if it is present
        in at least one directory.

        The order of the directories matters. First it is searched for
        the plugin in the main_dir. If the plugin is not found,
        the search proceeds in the other directories by their order.

        Parameters
        ----------
        name : str
            Name of requested Plugin.
        version : int
            Version of requested Plugin.

        Returns
        -------
            Plugin with the given name and version.

        Raises
        ------
        NeadsPluginNotFound
            When the plugin is not found in the pool (in none of the
            directories).
        """

        for pool in self._pools:
            try:
                return pool.get_plugin(name, version)
            except eh.NeadsPluginNotFound:
                pass
        else:
            raise eh.NeadsPluginNotFound(f"Plugin '{name}' with version"
                                         f" {version} was not found.")

    def _open(self):
        """Prepare the PluginPool for use.

        Read plugins into memory.
        """

        for pool in self._pools:
            pool.open()

    def _close(self):
        """End an active state of the PluginPool.

        Releases the loaded plugins.
        """

        for pool in self._pools:
            pool.close()
