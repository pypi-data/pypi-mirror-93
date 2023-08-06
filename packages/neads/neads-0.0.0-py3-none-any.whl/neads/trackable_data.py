"""Module providing TrackableData class for managed storage room for data.
"""
# TODO: very much incomplete, almost nothing is implemented

# TODO: ideally, there should be only two public methods
#  store_data, get_data (possibly just get, store)
#  -- if it is necessary, just have private methods for other actions
#     -- it is better to use private methods from MemoryManager
#     -- than explain which method use/not use anywhere else

from __future__ import annotations

from typing import TYPE_CHECKING
from neads.get_data_size import getsize

if TYPE_CHECKING:
    from neads.memory_manager import MemoryManager


class TrackableData:
    """Storage place for data produced by plugins."""

    def __init__(self, memory_manager: MemoryManager, tmp_file):
        self._memory_manager = memory_manager
        self._data = None
        self._are_data_present = False
        self._tmp_file = tmp_file
        # TODO: what exactly is "are_set"?
        self.are_set = False

    def get_data(self):
        if self._are_data_present:
            return self._data
        else:
            # Here will be something like '_mm.request_data(self)'
            raise NotImplementedError('Data should be always present.')

    def store_data(self, data):
        self.are_set = True
        self._data = data
        self._memory_manager.data_obtained(self)

    def keep_data(self):
        # TODO: check if needed, or make private
        self._are_data_present = True

    def shelve_data(self):
        # TODO: check if needed, or make private
        self._are_data_present = False
        # pickle data or something like that

    def load_data(self):
        # TODO: check if needed, or make private
        # unpickle data
        self._are_data_present = True
        pass

    def get_data_size(self):
        # TODO: check if needed, or make private
        if self._are_data_present:
            return getsize(self._data)
        else:
            return 0

