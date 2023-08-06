"""Module providing Database for storing data produced by plugins."""

# TODO: Database should be abstract class defining contract
#  this is just a one of possible implementations
#  !! after reorganization check that comments are still valid !!

# TODO: I wanted two steps - creation and then usage
#  now we have 3 steps - creation, init and open/close (which is usage)
#  think through whether the current schema is ideal

# TODO: write database as self-contained piece of code
#  it should have had implemented __open__ __exit__ protocols!

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from pathlib import Path
import os
import pickle as pkl  # for serializing the index file
import uuid
import shutil

from neads.database_serializer import Serializer, PickleSerializer
import neads.error_handlers.database_error_handler as eh
import neads.logger as logger

if TYPE_CHECKING:
    from neads.data_definition import DataDefinition


class Database:
    """Database for saving and retrieving data produced by plugins.

    The Database must be created first and the a Database instance can
    be initialized. Then, using context manager, it can store or
    retrieve data with given key, which is a DataDefinition of the data.

    Attributes
    ----------
    is_open : bool
        Says whether the database is open. That is, whether is ready for
        use. It is forbidden to load from closed database or save any
        data there.
    """

    DB_INDEX_FILENAME = 'index'
    DB_DATA_DIR = 'data'

    SERIALIZER: Serializer = PickleSerializer()

    @staticmethod
    def _db_index_filename(main_dir: Path) -> Path:
        """Return name of index file.

        Parameters
        ----------
        main_dir : Path
            Main directory of the database.

        Returns
        -------
        Path
            File name of index, where the names of files of particular
            data will be stored, provided that the given directory is
            a main directory of the database.
        """

        return main_dir / Database.DB_INDEX_FILENAME

    @staticmethod
    def _db_data_dir(main_dir: Path) -> Path:
        """Return name of directory for data files storage.

        Parameters
        ----------
        main_dir : Path
            Main directory of the database.

        Returns
        -------
        Path
            Directory where the data will be stored, provided that the
            given directory is a main directory of the database.
        """

        return main_dir / Database.DB_DATA_DIR

    @staticmethod
    def create_database(main_dir: Path):
        """Create a database layout in given directory.

        Creates an index file, which links database keys with files where
        the corresponding data are, and a directory for the data files.

        Parameters
        ----------
        main_dir
            Directory where the database should reside. It does not need
            to exist. However, if it does, it must be empty.

        Raises
        ------
        NeadsDatabaseError
            If the given directory is not empty.
        """

        if not os.path.exists(main_dir):
            os.mkdir(main_dir)

        if len(os.listdir(main_dir)) == 0:
            # Create index file
            with open(Database._db_index_filename(main_dir), 'wb') as f:
                pkl.dump({}, f)
            # Create dir for data
            os.mkdir(Database._db_data_dir(main_dir))
        else:
            raise eh.NeadsDatabaseError('The directory is not empty.')

    def __init__(self, main_dir: Path):
        """Initialize database object with given directory.

        It is assumed that there is created database in the given
        directory.

        Parameters
        ----------
        main_dir
            Directory, where the database is located.
        """

        # TODO: do some check like "everything is be okay"
        #  at least partially, ie. check that index file is present and
        #  so on
        self._main_dir = main_dir
        self._index = None
        self.is_open = False
        self._index_filename = self._db_index_filename(self._main_dir)
        self._data_dir = self._db_data_dir(self._main_dir)

    def open(self):
        """Prepare the database for use.

        Read the index file into memory.
        """
        if self.is_open:
            raise eh.NeadsDatabaseError('Database is already open.')

        with open(self._index_filename, 'rb') as f:
            self._index = pkl.load(f)
        self.is_open = True

    def close(self):
        """End active state of the Database."""
        if not self.is_open:
            raise eh.NeadsDatabaseIsNotOpen('Database is not open.')

        self.is_open = False
        with open(self._index_filename, 'wb') as f:
            pkl.dump(self._index, f)
        self._index = None

    def save(self, data: Any, data_definition: DataDefinition):
        """Save given data to database under given key.

        Parameters
        ----------
        data : Any
            Data to save.
        data_definition : DataDefinition
            Definition of data given in the first parameter. Serves as a
            database key.

        Raises
        ------
        NeadsDatabaseIsNotOpen
            When the Database is not open (was not called the method
            open).
        """

        if self.is_open:
            key = data_definition.to_hashable()
            if key not in self._index:
                filename = self._new_filename()
                self.SERIALIZER.save(data, filename)
                self._index[key] = filename
            else:
                assert data == self.SERIALIZER.load(self._index[key])
        else:
            raise eh.NeadsDatabaseIsNotOpen('Database must be open '
                                            'when saving data')

    def load(self, data_definition: DataDefinition) -> Any:
        """Return data corresponding to the given definition.

        Parameters
        ----------
        data_definition
            Definition of data to load. Serves as a database key.

        Returns
        -------
        Any
            Data that correspond to the given DataDefinition.

        Raises
        ------
        DataNotFound
            When the data for the given definition are not present in
            the database.

        NeadsDatabaseIsNotOpen
            When the Database is not open (was not called the method
            open).
        """

        if self.is_open:
            key = data_definition.to_hashable()
            try:
                filename = self._index[key]
                return self.SERIALIZER.load(filename)
            except KeyError as e:
                raise eh.DataNotFound() from e
        else:
            raise eh.NeadsDatabaseIsNotOpen('Database must be open '
                                            'when loading data')

    def _new_filename(self):
        """Generate new name filename."""
        # TODO: add check, whether the name is used (probably)
        return self._data_dir / str(uuid.uuid4())

    def _check_all_database_components(self):
        # TODO: checks that the index file and data dir is where is
        #  should be
        return NotImplementedError()

    def clean(self):
        if self.is_open:
            raise eh.NeadsDatabaseError('Database must be closed when '
                                        'cleaning.')

        shutil.rmtree(self._main_dir)
        Database.create_database(self._main_dir)
