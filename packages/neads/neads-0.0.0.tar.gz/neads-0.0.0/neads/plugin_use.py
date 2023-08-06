"""Module with class PluginUse, which is a prototype of an individual node.
"""

# TODO: i am pretty sure that the id is useless or, if it is used,
#  it shouldn't be

from __future__ import annotations

from typing import TYPE_CHECKING

from neads.data_definition import DataDefinitionComponent

if TYPE_CHECKING:
    from neads.plugin_record import PluginRecord
    from neads.plugin_pool import PluginPool


class PluginUse:
    """Description of desired plugin action, prototype of a node.

    Attributes
    ----------
    params : dict
        Params set with which the plugin will be called.
    """

    def __init__(self, plugin_record: PluginRecord, params: dict):
        """Initialize a PluginUse instance.

        Parameters
        ----------
        plugin_record
            Original description of the plugin corresponding with the
            PluginUse.
        params
            Params set with which the plugin will be called.
        """

        self._plugin_record = plugin_record
        self.params = params

    @property
    def name(self):
        """Name of the acting plugin."""
        return self._plugin_record.name

    @property
    def version(self):
        """Version of the acting plugin."""
        return self._plugin_record.version

    @property
    def method(self):
        """Method of the acting plugin. It need not to be specified."""
        return self._plugin_record.method

    @property
    def origin(self):
        """Return identification number of the record.

        This can be used for finding whether two PluginUses share the
        same PluginRecord.
        """

        # something as ID of PluginRecord from which it came
        return id(self._plugin_record)

    def get_plugin(self, plugin_pool: PluginPool):
        """Return plugin method of the corresponding plugin.

        Parameters
        ----------
        plugin_pool : PluginPool
            PluginPool where to search for the plugin, if the PluginUse
            does not held the method directly.

        Returns
        -------
        Plugin method of the corresponding plugin.
        """

        # TODO: add appropriate exception, if the plugin is not used
        if self.method:
            return self.method
        else:
            return plugin_pool.get_plugin(self.name, self.version).method

    @property
    def get_data_definition_component(self):
        """Return DDC of the action a plugin described be the PluginUse."""
        return DataDefinitionComponent(self)

    @property
    def plugin_type(self):
        """Return type of the plugin."""
        return self._plugin_record.plugin_type

    @property
    def phase_type(self):
        """Return type in which the plugin appears."""
        return self._plugin_record.phase_type
