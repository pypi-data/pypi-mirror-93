"""Module providing class Node, ie. the building block of NeadsGraph."""

from __future__ import annotations

from typing import TYPE_CHECKING, Union, Iterable

from neads.data_definition import DataDefinition, DataDefinitionComponent

if TYPE_CHECKING:
    from neads.plugin_use import PluginUse
    from neads.neads_graph import NeadsGraph
    from neads.plugin_pool import PluginPool


class Node:
    """Base class for all nodes in NeadsGraph and its subclasses.

    Attributes
    ----------
    parents : [Node]
        All nodes from which the node get its data.
    children : [Node]
        All nodes that get their data from the node.
    graph : NeadsGraph
        Graph to which the node belongs.
    """

    def __init__(self, plugin_use: PluginUse, graph: NeadsGraph):
        """Initialize Node with its basic description.

        The nodes will have no relatives, ie. no parents nor children.

        Parameters
        ----------
        plugin_use : PluginUse
            Description of local modification of data by the node.
        graph : NeadsGraph
            Graph to which the node belongs.
        """

        # TODO: do not provide direct access to plugin_use
        #  make it private and use properties for making available the
        #  important information (and update the comments)

        # TODO: probably redefine parents / children relation
        self.parents: [Node] = []
        self.children: [Node] = []

        self.plugin_use = plugin_use
        self.graph = graph

    def attach_children(self, nodes: Union[Iterable[Node], Node]):
        """Mutually attach the given nodes as a children.

        The node will be added to parents lists of the given nodes. The
        method can take just an instance of Node.

        Parameters
        ----------
        nodes
            One or more nodes to be attached as children of the node.
        """

        if isinstance(nodes, Node):
            nodes = [nodes]

        self.children.extend(nodes)
        for node in nodes:
            node.parents.append(self)

    def get_plugin(self, plugin_pool: PluginPool):
        """Return corresponding plugin method.

        If the plugin method was specified directly via function,
        the function is returned. In the other case, Plugin method is
        extracted from the given PluginPool.

        Parameters
        ----------
        plugin_pool
            PluginPool where to search for corresponding plugin, if the
            method was not directly specified.

        Returns
        -------
            Plugin method of the corresponding plugin.
        """

        # TODO: rename not plugin, but plugin method
        # TODO: probably raises something, add to comments
        return self.plugin_use.get_plugin(plugin_pool)

    def get_data_definition(self) -> DataDefinition:
        """Return self DataDefinition."""
        return DataDefinition(self)

    def get_data_definition_component(self) -> DataDefinitionComponent:
        """Return self DataDefinitionComponent."""
        return self.plugin_use.get_data_definition_component

    def get_depth(self):
        """Return depth in the graph.

        The depth of a node is computed as a maximum from parents depths
        incremented by one. Zero, if a node has no parents.
        """

        if self.parents:
            return max([p.get_depth() for p in self.parents]) + 1
        else:
            return 0
