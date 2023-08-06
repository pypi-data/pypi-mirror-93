"""Module providing unified interface to various serializers.

Only PickleSerializer, which uses pickle, is available so far.
"""

from typing import Any, Union
import os
from abc import ABC, abstractmethod
import pickle as pkl

PathLike = Union[str, bytes, os.PathLike]


class Serializer(ABC):
    """Interface stating what a 'serializer' is.

    It needs to have two methods described in their own documentation.
    """

    @abstractmethod
    def save(self, data: Any, filename: PathLike):
        """Save data into a file with the given name.

        Parameters
        ----------
        data
            Data to save to the file.
        filename
            Name of the file where the data will be saved.
        """

        pass

    @abstractmethod
    def load(self, filename: PathLike) -> Any:
        """Load and return data from a file with the given name.

        Parameters
        ----------
        filename
            Name of the file from which the data will be loaded.

        Returns
        -------
        Any
            Loaded data, ie. content of the file.
        """

        pass


class PickleSerializer(Serializer):
    """Serializer which uses pickle for saving / loading data."""

    def save(self, data: Any, filename: PathLike):
        """Save data into a file with the given name.

        Uses a pickle.dump method. Raises an exception when the data
        cannot be pickled. However, as the documentation of pickle lacks
        a list of possible exception, they cannot be listed here.

        Parameters
        ----------
        data : Any
            Data to save to the file.
        filename : PathLike
            Name of the file where the data will be saved.
        """

        with open(filename, 'wb') as f:
            pkl.dump(data, f)

    def load(self, filename: PathLike) -> Any:
        """Load and return data from a file with the given name.

        Uses a pickle.load method. Raises an exception when the data
        cannot be unpickled. However, as the documentation of pickle
        lacks a list of possible exception, they cannot be listed here.

        Parameters
        ----------
        filename : PathLike
            Name of the file from which the data will be loaded.

        Returns
        -------
        Any
            Loaded data, ie. content of the file.
        """

        with open(filename, 'rb') as f:
            return pkl.load(f)
