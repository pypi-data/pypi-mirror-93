"""Module providing the Project class, entrance to using neads."""

from __future__ import annotations

from typing import TYPE_CHECKING
from pathlib import Path
import os
from time import time

from neads.computation_manager import SingleThreadedComputationManager
from neads.plugin_pool import CascadedPluginPool
from neads.database import Database
from neads.metadata import Metadata
import neads.error_handlers.project_error_handler as eh
import neads.logger as logger

if TYPE_CHECKING:
    from neads.configuration import Configuration
    from neads.computation_manager import ComputationManager
    from neads.plugin_pool import PluginPool


class Project:
    """Entrance to using Neads.

    Project contain a database of intermediate results from previous
    computations, plugin pool (database of plugins) and directory with
    logs from the computations.

    Database is fully administered by Nead,s and it is not advised to
    make any changes by hand there. Project provides a method for
    cleaning the content of the database.

    Plugin pool (directory :code:`/plugins`) contains plugins. Neads
    considers any file with the extension *.py* to be a plugin, if it is
    located somewhere in the directory. Thus, the layout of the plugin
    directory (that is, organization of plugins in subdirectories) may be
    arbitrary.

    Apart from plugins *local* plugins of the Project, it is possible to
    use plugins in the central plugin pool for computation.

    Logs show progress of previous computations and by default, their
    filename is derived from the Unix time of start of the
    particular computation.

    Metadata file is there only for forward compatibility. It currently
    serves no purpose.
    """

    _PROJECT_CONTENT = {
        'plugin_pool': 'plugins',
        'database': 'database',
        'metadata': 'metadata',
        'tmp_dir': 'tmp',
        'log_dir': 'log'
    }
    computation_manager_factory: ComputationManager = \
        SingleThreadedComputationManager
    database_factory: Database = Database
    plugin_pool_factory: PluginPool = CascadedPluginPool

    @staticmethod
    def _project_database_dir(directory: Path) -> Path:
        """Return path to database dir with respect to the given dir."""
        return directory / Project._PROJECT_CONTENT['database']

    @staticmethod
    def _project_plugin_pool_dir(directory: Path) -> Path:
        """Return path to plugin pool dir with respect to the given dir."""
        return directory / Project._PROJECT_CONTENT['plugin_pool']

    @staticmethod
    def _project_metadata_dir(directory: Path) -> Path:
        """Return path to metadata file with respect to the given dir."""
        return directory / Project._PROJECT_CONTENT['metadata']

    @staticmethod
    def _project_tmp_dir(directory: Path) -> Path:
        """Return path to tmp dir with respect to the given dir."""
        return directory / Project._PROJECT_CONTENT['tmp_dir']

    @staticmethod
    def _project_log_dir(directory: Path) -> Path:
        """Return path to log dir with respect to the given dir."""
        return directory / Project._PROJECT_CONTENT['log_dir']

    @staticmethod
    def create_project(directory: Path):
        """Create a Project in the given directory.

        All contents of the Project is empty. That is, no data are stored
        in the database, plugin pool directory is blank as well as the
        directory for logs.

        However, it is possible to use the standard plugins in central
        plugin pool.

        Parameters
        ----------
        directory : Path
            Directory where to create the project. If it does not exist,
            it will be created. If it exists, it must be empty.

        Raises
        ------
        NeadsCannotCreateProject
            The given directory is not empty.
        """

        if directory.exists():
            if not directory.is_dir():
                # TODO: add this kind of check to DB, PP and Meta
                raise eh.NeadsInvalidProjectDirectoryError(
                    f'Argument is not dir: {directory}')
            elif os.listdir(directory):
                raise eh.NeadsInvalidProjectDirectoryError(
                    f'Directory is not empty: {directory}')
        else:
            os.mkdir(directory)

        # TODO: this probably can be done in more elegant way
        os.mkdir(Project._project_metadata_dir(directory))
        Metadata.create_metadata(
            Project._project_metadata_dir(directory)
        )

        os.mkdir(Project._project_database_dir(directory))
        Project.database_factory.create_database(
            Project._project_database_dir(directory)
        )

        os.mkdir(Project._project_plugin_pool_dir(directory))
        Project.plugin_pool_factory.create_plugin_pool(
            Project._project_plugin_pool_dir(directory)
        )

        os.mkdir(Project._project_log_dir(directory))

    @property
    def database_dir(self):
        return self._project_database_dir(self.main_dir)

    @property
    def plugin_pool_dir(self):
        return self._project_plugin_pool_dir(self.main_dir)

    @property
    def metadata_dir(self):
        return self._project_metadata_dir(self.main_dir)

    @property
    def tmp_dir(self):
        return self._project_tmp_dir(self.main_dir)

    @property
    def log_dir(self):
        return self._project_log_dir(self.main_dir)

    def __init__(self, main_dir):
        """Initialize a Project instance.

        It is assumed that main_dir contains a healthy Project with a
        proper layout. The method does **not** create a new Project.

        Parameters
        ----------
        main_dir
            Directory with a location of the project.
        """

        # TODO: really feel that all most of these attributes should be
        #  private
        self.main_dir = Path(main_dir)
        self.plugin_pool = self.plugin_pool_factory(
            self.plugin_pool_dir
        )
        self.database = self.database_factory(
            self.database_dir
        )
        self.metadata = Metadata(
            self.metadata_dir
        )
        self._is_open = False

    def compute(self, cfg: Configuration,
                log_file='default', log_to_stdout=False):
        """Perform computation according the given configuration.

        The method creates a tree of intermediate results and evaluates it.

        A log is recorded to capture the progress of the computation. By
        default, a new file in log directory is created for that purpose.

        However, it is possible to reroute the log output to different
        file giving its path in log-file parameter. On the other hand, it
        is not possible to not create any log at all. The log will
        always be printed to a file.

        Also, the log may be displayed via the standard output,
        if specified.

        During computation, all intermediate results are stored in the
        database, while the final results (i.e. results of finalizers)
        are not. When running a computation next time (possibly with
        a different configuration), the intermediate results which are
        common to both configurations are loaded from the database in an
        intelligent manner (i.e. only the data which is necessary to load
        are loaded). Then they are used to produce the final results.

        Notice that only results of Finalizers are considered to be the
        final results. That is, if the Finalizers are not present in the
        configuration, it is likely that no actual computation will run.

        Parameters
        ----------
        cfg : Configuration
            Description of computed process.
        log_file
            To which file will be progress of computation logged. By
            leaving the value 'default', a new file will be created in
            log directory with a current timestamp as its name.
        log_to_stdout : bool
            Whether to print the log messages to standard output.
        """

        # TODO: use metadata somehow
        if not self._is_open:
            raise eh.NeadsProjectIsNotOpen('Project must be open '
                                            'running computation')

        self._set_up_logging(log_file, log_to_stdout)
        logger.info('Call computation method', 1)
        try:
            os.mkdir(self.tmp_dir)
            cm = self.computation_manager_factory(self.database,
                                                  self.plugin_pool,
                                                  self.tmp_dir)
            cm.compute(cfg)
        finally:
            os.rmdir(self.tmp_dir)
            logger.info('End computation method', -1)
            self._tear_down_logging()

    def clean_database(self):
        """Remove content of database.

        The database is put in the initial state, i.e. it does not
        contain any data. The rest of the Project remains untouched.
        """

        self.database.clean()

    def __enter__(self):
        """Activate the Project instance.

        Loads important pieces of database into memory and checks
        available plugins.

        Returns
        -------
        Project
            Self.
        """

        self.database.open()
        self.plugin_pool.open()
        self._is_open = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Turn Project instance to an inactive mode."""
        self._is_open = False
        self.database.close()
        self.plugin_pool.close()

    def _set_up_logging(self, log_file, log_to_stdout):
        """Set up logging for the computation.

        log_file
            To which file will be a progress of computation logged. By
            leaving the value 'default', a new file will be created in
            log directory with a current timestamp as its name.
        log_to_stdout : bool
            Whether to print the log messages to standard output.
        """

        if log_file == 'default':
            log_file = self.log_dir / str(time())
        logger.set_up_logging(log_file, log_to_stdout)

    def _tear_down_logging(self):
        # to enable use in JupyterNB
        # TODO: really that drastically?
        logger.shut_down()
