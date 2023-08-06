"""Module with factory for executable nodes."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from neads.node_factory import NodeFactory
from neads.executable_nodes import ExecutableNode, ExecutableEvolver, \
    ExecutableFinalizer
import neads.logger as logger

if TYPE_CHECKING:
    from neads.trackable_data import TrackableData
    from neads.plugin_use import PluginUse


class ExecutableNodeFactory(NodeFactory):
    """NodeFactory for executable nodes.

    Executable nodes can be created via this factory class.
    """

    def __init__(self, trackable_data_source: Callable[[], TrackableData]):
        logger.info('Start executable node factory initialization', 1)
        super().__init__()
        self.trackable_data_source = trackable_data_source
        logger.info('End executable node factory initialization', -1)

    def create_loader(self, loader: PluginUse) -> ExecutableNode:
        """Create node for the given loader.

        Parameters
        ----------
        loader : PluginUse
           PluginUse describing the node.

        Returns
        -------
        ExecutableNode
            Created node with plugin, version and params borrowed from
            the given PluginUse.
        """

        return self._create_standard_executable(loader)

    def create_preprocessor(self, preprocessor: PluginUse) \
            -> ExecutableNode:
        """Create node for the given preprocessor.

        Parameters
        ----------
        preprocessor : PluginUse
           PluginUse describing the node.

        Returns
        -------
        ExecutableNode
            Created node with plugin, version and params borrowed from
            the given PluginUse.
        """

        return self._create_standard_executable(preprocessor)

    def create_evolver(self, evolver: PluginUse) -> ExecutableEvolver:
        """Create node for the given evolver.

        Parameters
        ----------
        evolver : PluginUse
           PluginUse describing the node.

        Returns
        -------
        ExecutableEvolver
            Created node with plugin, version and params borrowed from
            the given PluginUse.
        """

        # TODO: give the trackable_data directly, not a source
        return ExecutableEvolver(evolver, self.graph,
                                 self.trackable_data_source)

    def create_extractor(self, extractor: PluginUse) -> ExecutableNode:
        """Create node for the given extractor.

        Parameters
        ----------
        extractor : PluginUse
           PluginUse describing the node.

        Returns
        -------
        ExecutableNode
            Created node with plugin, version and params borrowed from
            the given PluginUse.
        """

        return self._create_standard_executable(extractor)

    def create_builder(self, builder: PluginUse) -> ExecutableNode:
        """Create node for the given builder.

        Parameters
        ----------
        builder : PluginUse
           PluginUse describing the node.

        Returns
        -------
        ExecutableNode
            Created node with plugin, version and params borrowed from
            the given PluginUse.
        """

        return self._create_standard_executable(builder)

    def create_weighted_editor(self, weighted_editor: PluginUse) \
            -> ExecutableNode:
        """Create node for the given weighted editor.

        Parameters
        ----------
        weighted_editor : PluginUse
           PluginUse describing the node.

        Returns
        -------
        ExecutableNode
            Created node with plugin, version and params borrowed from
            the given PluginUse.
        """

        return self._create_standard_executable(weighted_editor)

    def create_filter(self, filter: PluginUse) -> ExecutableNode:
        """Create node for the given filter.

        Parameters
        ----------
        filter : PluginUse
           PluginUse describing the node.

        Returns
        -------
        ExecutableNode
            Created node with plugin, version and params borrowed from
            the given PluginUse.
        """

        return self._create_standard_executable(filter)

    def create_unweighted_editor(self, unweighted_editor: PluginUse) \
            -> ExecutableNode:
        """Create node for the given unweighted editor.

        Parameters
        ----------
        unweighted_editor : PluginUse
           PluginUse describing the node.

        Returns
        -------
        ExecutableNode
            Created node with plugin, version and params borrowed from
            the given PluginUse.
        """

        return self._create_standard_executable(unweighted_editor)

    def create_analyzer(self, analyzer: PluginUse) -> ExecutableNode:
        """Create node for the given analyzer.

        Parameters
        ----------
        analyzer : PluginUse
           PluginUse describing the node.

        Returns
        -------
        ExecutableNode
            Created node with plugin, version and params borrowed from
            the given PluginUse.
        """

        return self._create_standard_executable(analyzer)

    def create_finalizer(self, finalizer: PluginUse) \
            -> ExecutableFinalizer:
        """Create node for the given finalizer.

        Parameters
        ----------
        finalizer : PluginUse
           PluginUse describing the node.

        Returns
        -------
        ExecutableFinalizer
            Created node with plugin, version and params borrowed from
            the given PluginUse.
        """

        # TODO: give the trackable_data directly, not a source
        return ExecutableFinalizer(finalizer, self.graph,
                                   self.trackable_data_source)

    def _create_standard_executable(self, plugin_use: PluginUse) \
            -> ExecutableNode:
        """Create node for the given plugin use.

        Parameters
        ----------
        plugin_use : PluginUse
           PluginUse describing the node.

        Returns
        -------
        ExecutableNode
            Created node with plugin, version and params borrowed from
            the given PluginUse.
        """

        # TODO: give the trackable_data directly, not a source
        return ExecutableNode(plugin_use, self.graph,
                              self.trackable_data_source)

    # TODO: create the most general method for creation of nodes
    #  class_(plugin, self.graph, self.trackable_data_source)
