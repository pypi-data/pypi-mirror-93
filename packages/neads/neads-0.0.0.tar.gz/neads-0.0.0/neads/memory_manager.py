"""Module providing MemoryManagers for managing data produced by plugins.

The idea of MemoryManager is that it is a class that manages a data
produced by plugins to avoid memory overflow. In case of need,
the MemoryManager may decide to shelve some data to tmp files to release
some memory.

The difference between MemoryManager a system swapping is in the fact
that MemoryManager is able to do a smart swapping considering which data
will and won't needed in near future. If a particular data won't be
needed at all, it can release them.

The main class MemoryManager prescribes a contract which must be follow
by its subclasses.
"""
# TODO: MemoryManager should be an abstract class for specifying the
#  contract
#  with subclass LoggingMemoryManager implementing this algorithm
#  ie. same relation as is for ComputationManager and SingleThreadedCM
#  !! then check, that all comments are still valid !!

# TODO: probably will be a listener of events of CM so that it can see
#  which data instances are no longer needed and which will be
#  -- as a possible proposition, there may be other ways as explicit
#     signaling but with other problems

# TODO: maybe change terminology from "data instance" to "data unit",
#  because "instance" might be a confusing term

# TODO: there is a notification (data_obtained) the MM that a new data
#  arrived, but there is no method for notification that a particular
#  data need to be recovered, ie. loaded from tmp file to be used.

from pathlib import Path
from time import time

from neads.trackable_data import TrackableData
import neads.logger as logger


class MemoryManager:
    """Class managing all data instances produced by plugins.

    The MemoryManager issue data instances for all data produces by
    plugins. Therefore it has an awareness of all these data.

    This particular MemoryManager only logs the current size of these
    data instances in memory. In future versions it should be able to
    manage these instances to prevent memory overflow.
    """

    def __init__(self, tmp_directory: Path):
        """Initialize the MemoryManager with a directory for tmp files.

        Parameters
        ----------
        tmp_directory
            Directory for tmp files where the data might be stored when
            the memory is close to be full.
        """

        logger.info('Start memory manager initialization', 1)
        self._data_instances = []
        self._directory = tmp_directory
        logger.info('End memory manager initialization', -1)

    def issue_data_instance(self) -> TrackableData:
        """Return a new data instance tracked by the MemoryManager.

        Returns
        -------
            TrackableData instance tracked by the MemoryManager.
        """

        # TODO: the system for name generation must be changed and moved
        #  to separate method
        new_instance = TrackableData(self, self._directory / str(time()))
        self._data_instances.append(new_instance)
        return new_instance

    def data_obtained(self, data_instance: TrackableData):
        """Notify the manager that given data instance obtained some data.

        As it is a change of state of the memory, the MemoryManager may
        take some actions. In this case, it only logs the current size
        of registered data instances.

        Parameters
        ----------
        data_instance
            Data instance that obtained some data.
        """

        data_instance.keep_data()
        data_size = sum([data_inst.get_data_size()
                         for data_inst in self._data_instances])
        logger.info(f'Current size of data instances in memory is '
                    f'{data_size}', 0)
