"""Module providing ComputationGraph for ComputationManager."""

# TODO: graph-querying methods should be probably in NeadsGraph
#  at least the general
#  the specialized 'get_evolvers', 'get_finalizer' may possibly stay here

from __future__ import annotations

from typing import TYPE_CHECKING, Set, Callable
from neads.neads_graph import NeadsGraph
from neads.plugin_record import PluginType
import neads.logger as logger

if TYPE_CHECKING:
    from neads.configuration import Configuration
    from neads.executable_node_factory import ExecutableNodeFactory
    from neads.executable_nodes import ExecutableEvolver, \
        ExecutableFinalizer, ExecutableNode


class ComputationGraph(NeadsGraph):
    def __init__(self,
                 configuration: Configuration,
                 node_factory: ExecutableNodeFactory):
        logger.info('Start computation graph initialization', 1)
        super().__init__(configuration, node_factory)
        logger.info('End computation graph initialization', -1)

    def get_evolvers(self) -> Set[ExecutableEvolver]:
        """Return all evolvers in the graph."""
        # TODO: solve typing issues
        return self._select_plugins_by_type(PluginType.EVOLVER)

    def get_finalizers(self) -> Set[ExecutableFinalizer]:
        """Return all finalizers in the graph."""
        # TODO: solve typing issues
        return self._select_plugins_by_type(PluginType.FINALIZER)

    def _select_plugins_by_type(self, plugin_type: PluginType) \
            -> Set[ExecutableNode]:
        """Querying method based on given PluginType.

        Parameters
        ----------
        plugin_type
            PluginType to determine which nodes should be returned.

        Returns
        -------
        Set[ExecutableNode]
            All nodes that have the given type.
        """

        return self._select_plugins_by_condition(
            lambda node: node.plugin_use.plugin_type == plugin_type
        )

    def _select_plugins_by_condition(
            self,
            condition: Callable[[ExecutableNode], bool]
    ) -> Set[ExecutableNode]:
        """General querying method based on given condition.

        Parameters
        ----------
        condition
            Condition for selecting which nodes will be returned.

        Returns
        -------
        Set[ExecutableNode]
            All nodes that satisfy the given condition.
        """

        def visit(node):
            if condition(node):
                to_return.add(node)

            visited.add(node)
            for child in node.children:
                if child not in visited:
                    visit(child)

        visited = set()
        to_return = set()
        for initial_node in self.first_layer:
            visit(initial_node)
        return to_return
