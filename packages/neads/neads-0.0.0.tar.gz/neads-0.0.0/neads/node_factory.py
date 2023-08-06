"""Module with base class for all NodeFactories."""

# TODO: think whether do not create at least nodes
#  or just point each method to one 'general' method as it is in
#  executable_nodes_factory (exactly for easier implementation of other
#  factories)

from __future__ import annotations

from typing import TYPE_CHECKING, Union

from abc import abstractmethod, ABC

if TYPE_CHECKING:
    from neads.neads_graph import NeadsGraph
    from neads.plugin_use import PluginUse
    from neads.nodes import Node


class NodeFactory(ABC):
    """Abstract base class for all NodeFactories.

    Via NodeFactory, it is possible to specify how the nodes of a
    NeadsGraph should be created.

    Attributes
    ----------
    graph : Union[NeadsGraph, None]
        Graph to which the created nodes belong. Must be specified with
        'bind_graph' method.
    """

    def __init__(self):
        """Initialize the node factory."""
        self.graph: Union[NeadsGraph, None] = None

    def bind_graph(self, graph: NeadsGraph):
        """Bound the given graph to the factory.

        Parameters
        ----------
        graph : NeadsGraph
            Graph to which the created nodes will belong.
        """

        # TODO: allow to specify the graph just once
        self.graph = graph

    # TODO: for all method -> check first that a graph was bound
    #  also do typing

    @abstractmethod
    def create_loader(self, loader: PluginUse) -> Node:
        pass

    @abstractmethod
    def create_preprocessor(self, preprocessor: PluginUse) -> Node:
        pass

    @abstractmethod
    def create_evolver(self, evolver: PluginUse) -> Node:
        pass

    @abstractmethod
    def create_extractor(self, extractor: PluginUse) -> Node:
        pass

    @abstractmethod
    def create_builder(self, builder: PluginUse) -> Node:
        pass

    @abstractmethod
    def create_weighted_editor(self, weighted_editor: PluginUse) -> Node:
        pass

    @abstractmethod
    def create_filter(self, filter: PluginUse) -> Node:
        pass

    @abstractmethod
    def create_unweighted_editor(self, unweighted_editor: PluginUse) \
            -> Node:
        pass

    @abstractmethod
    def create_analyzer(self, analyzer: PluginUse) -> Node:
        pass

    @abstractmethod
    def create_finalizer(self, finalizer: PluginUse) -> Node:
        pass
