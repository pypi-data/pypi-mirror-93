"""Module providing the Metadata class to adjust computation process."""

# TODO: put metadata in use

import json
from pathlib import Path


class Metadata:
    """Enable to user to adjust the computation process."""

    METADATA_FILENAME = 'metadata.json'
    DEFAULT_METADATA = {
        'version': 'plugin'
    }

    @staticmethod
    def create_metadata(directory: Path):
        """Create default metadata in the given directory.

        Parameters
        ----------
        directory
            Directory where to create the metadata.
        """
        with open(directory / Metadata.METADATA_FILENAME, 'w') as f:
            json.dump(Metadata.DEFAULT_METADATA, f)

    @staticmethod
    def load_in_directory(directory):
        # TODO: wtf?
        with open(directory / Metadata.METADATA_FILENAME, 'r') as f:
            metadata = json.load(f)
            return Metadata(**metadata)

    def __init__(self, version):
        # TODO: wtf?
        self.version = version
