"""Module providing mixin for phases for logging purposes."""

import neads.logger as logger


class PhaseLogMixin:
    @property
    def _log_name(self) -> str:
        return self.__class__.__name__.lower()

    def _log_start_creating_layer(self):
        logger.info(f'Start creating {self._log_name} layer', 1)

    def _log_end_creating_layer(self):
        logger.info(f'End creating {self._log_name} layer', -1)