"""Module with executable nodes, ie. building blocks of ComputationGraph.

The ExecutableNode class is a fully functioning base class with two
subclasses for required adjustment of behaviour. One is ExecutableEvolver,
because Evolvers need to be expanded, when they have their data. The
other is ExecutableFinalizer, as finalizers data are not stored in the
database.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable
import copy

from neads.nodes import Node
import neads.error_handlers.database_error_handler as db_eh
from neads.plugin_record import PluginType

if TYPE_CHECKING:
    from neads.trackable_data import TrackableData
    from neads.database import Database
    from neads.plugin_pool import PluginPool


class ExecutableNode(Node):
    """Base class of all executable node classes.

    Although it is called a base class, it is fully capable to work as
    it is, ie. subclasses are needed only for adjusting the behaviour.
    """

    def __init__(self, plugin_use, graph,
                 trackable_data_source: Callable[[], TrackableData]):
        """Initialize ExecutableNode with its basic description.

        The nodes will have no relatives, ie. no parents nor children.

        plugin_use : PluginUse
            Description of local modification of data by the node.
        graph : NeadsGraph
            Graph to which the node belongs.
        trackable_data_source : Callable[[], TrackableData]
            Source to TrackableData bound to the appropriate
            MemoryManager.
        """

        # TODO: wouldn't be better to obtain the TrackableData directly?
        super().__init__(plugin_use, graph)
        self._data: TrackableData = trackable_data_source()

    @property
    def data(self):
        """Return data held by the node."""
        return self._data.get_data()

    @data.setter
    def data(self, value):
        """Set data of the node.

        Parameters
        ----------
        value
            New data of the node.
        """

        self._data.store_data(value)

    def execute(self, database: Database, plugin_pool: PluginPool):
        """Evaluate the node.

        Takes the plugin method to compute output of the node. Then
        saves the data to the given database.

        Parameters
        ----------
        database : Database
            Database where to try to store the obtained data.
        plugin_pool : PluginPool
            Where to find the plugin method, if it was not specified
            directly.
        """

        self._do_execution(database, plugin_pool, save=True)
    
    def try_load(self, database: Database) -> bool:
        """Try to load the corresponding data from the given Database.

        Parameters
        ----------
        database : Database
            Database where to search for the data.

        Returns
        -------
        bool
            True, if the data were found. False otherwise.
        """

        try:
            self.data = database.load(self.get_data_definition())
            return True
        except db_eh.DataNotFound:
            return False

    def _do_execution(self, database: Database, plugin_pool: PluginPool,
                      save: bool):
        """Actually does the execution.

        Parameters
        ----------
        plugin_pool : PluginPool
            Where to find the plugin method, if it was not specified
            directly.

        Notes
        -----
            This method exists for easier implementation of the 'execute'
            method in ExecutableFinalizer.
        """

        arguments = self._get_arguments()
        self.data = self.get_plugin(plugin_pool)(**arguments)
        # TODO: move this part to 'execute' method
        #  then remove the db and save parameter
        #  it will be much more elegant
        #  then update comments
        if save:
            database.save(self.data, self.get_data_definition())

    def _get_arguments(self):
        """Return proper arguments for the corresponding plugin.

        Returns
        -------
        dict
            Arguments in a dictionary form.
        """

        # TODO: solve naming problem arguments vs. params
        arguments = copy.deepcopy(self.plugin_use.params)
        arguments['data'] = self._get_data_argument()
        return arguments

    def _get_data_argument(self):
        """Return proper 'data' argument for the corresponding plugin.

        Returns
        -------
            For each parent, it is a tuple (DataDefinition, Data). If
            there is only one parent, only the tuple is returned. In
            case of more parents, a list of tuples is returned. If the
            node does not have any parent, None is returned.
        """

        # TODO: seems too complicated
        if len(self.parents) > 1:
            source_data = []
            for parent in self.parents:
                source_data.append((parent.get_data_definition(),
                                    parent.data))
            return source_data
        elif len(self.parents) == 1:
            parent = self.parents[0]
            return parent.get_data_definition(), parent.data
        else:
            return None

    def __str__(self):
        # TODO: this was only for documentation purposes
        if self.plugin_use.plugin_type != PluginType.LOADER:
            name = self.plugin_use.name + ', ' + str(
                self.plugin_use.params)
        else:
            name = self.plugin_use.name
        return '(' + name + ')'


class ExecutableEvolver(ExecutableNode):
    """Subclass of ExecutableNode for evolvers.

    Evolvers need to be expanded when they get their data. This class
    alters the involved methods.

    Attributes
    ----------
    expanded : bool
        Whether the EvolverNode was already expanded, ie. whether
        remainder of the graph was constructed.
    """

    def __init__(self, plugin_use, graph, trackable_data_source):
        """Initialize ExecutableEvolver with its basic description.

        The nodes will have no relatives, ie. no parents nor children.

        plugin_use : PluginUse
            Description of local modification of data by the node.
        graph : NeadsGraph
            Graph to which the node belongs.
        trackable_data_source : Callable[[], TrackableData]
            Source to TrackableData bound to the appropriate
            MemoryManager.
        """

        super().__init__(plugin_use, graph, trackable_data_source)
        self.expanded = False

    def execute(self, database, plugin_pool):
        """Evaluate and expand the node.

        Takes the plugin method to compute output of the node and
        saves the data to the given database. Then expand self.

        Parameters
        ----------
        database : Database
            Database where to try to store the obtained data.
        plugin_pool : PluginPool
            Where to find the plugin method, if it was not specified
            directly.
        """

        super().execute(database, plugin_pool)
        self._expand()

    def try_load(self, database):
        # TODO: why the condition 'not self._data.are_set'?
        #  once I will find out, add docstring
        #  -- maybe they was already loaded by a parent?
        if not self._data.are_set:
            loaded = super().try_load(database)
            if loaded:
                self._expand()
            return loaded
        else:
            return True

    def _expand(self):
        """Create extractors and rest of the branch under the node."""

        interval_count = self._get_interval_count()
        self.graph.expand_evolver(self, interval_count)

    def _get_interval_count(self):
        """Return number of intervals in evolution."""
        return len(self.data['data'])  # data are sequence of intervals


class ExecutableFinalizer(ExecutableNode):
    """Subclass of ExecutableNode for finalizers.

    Data of finalizers are not stored nor loaded to/from database and
    the involved methods are altered here.
    """

    def execute(self, database, plugin_pool):
        """Evaluate the node.

        Takes the plugin method to compute output of the node.

        Parameters
        ----------
        database : Database
            Excessive parameter only for API compliance with 'execute'
            method of ExecutableNode.
        plugin_pool : PluginPool
            Where to find the plugin method, if it was not specified
            directly.
        """

        self._do_execution(database, plugin_pool, save=False)

    def try_load(self, database):
        """Return False, as Finalizers data are not stored in database."""
        return False
