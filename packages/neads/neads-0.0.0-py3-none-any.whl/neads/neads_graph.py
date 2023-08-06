"""Module providing the most general type of graph - NeadsGraph."""

# TODO: whole graph should be created ! inside configuration !

# TODO: then review the docstring, they are quite sloppy

# TODO: consider one virtual TOP vertex as the only one without parents
#  it may be valuable even for the new DataDefinition

# TODO: consider DFS creation of layers instead of BFS
#  it seems more flexible

# TODO: consider where should appear implementation of expansion
#  again - probably as a part of configuration

# TODO: consider redefining what a parent-child relation

# TODO: imagine that there can be more kinds Configuration and more
#  kinds of PluginRecord (PluginUse will stay)
#  make the implementation such that this is the case (do not rely on
#  maybe just a temporal fact that only the 'standard' Configuration is
#  used)


from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

import neads.error_handlers.neads_graph_error_handler as eh
import neads.logger as logger

if TYPE_CHECKING:
    from neads.nodes import Node
    from neads.phases import Phase
    from neads.configuration import Configuration
    from neads.node_factory import NodeFactory


class NeadsGraph:
    """Base class for all graph describing required operations from user.

    Attributes
    ----------
    node_factory : NodeFactory
        Factory class for creating graph nodes.
    configuration : Configuration
        Original description of structure of the graph.
    is_evolving : bool
        True, if evolving networks are supposed to be created.
    first_layer : [Node]
        Top most nodes, ie. the nodes without parents.
    """

    def __init__(self,
                 configuration: Configuration,
                 node_factory: NodeFactory):
        """Initialize NeadsGraph.

        Parameters
        ----------
        configuration
            Prescription of the graph.
        node_factory
            Source of nodes that will belong to the graph.
        """

        logger.info('Start neads graph initialization', 1)
        self.node_factory = node_factory
        node_factory.bind_graph(self)

        self.configuration = configuration
        self.is_evolving = configuration.is_evolving

        # number of evolvers still to expand before finalizers creation
        # finalizers are created when this counter drops to 0
        # i.e. non-evolving networks are build the whole graph directly
        self._evolvers_to_expand = 0 if not self.is_evolving else None
        self._last_layer_from_expansion = []

        # for simple expression in _build_graph
        self._developing_phases = [
            self.configuration.preprocessing,
            self.configuration.evolution,
            self.configuration.building,
            self.configuration.weighted_editing,
            self.configuration.filtering,
            self.configuration.unweighted_editing,
            self.configuration.analyzing,
        ]

        div_idx = self._developing_phases.index(
            self.configuration.evolution) + 1
        self._phases_up_to_evolution = self._developing_phases[:div_idx]
        self._phases_after_evolution = self._developing_phases[div_idx:]

        # Entry vertices of the actual graph
        self.first_layer: [Node] = []  # will be immediately assigned
        self._build_graph()
        logger.info('End neads graph initialization', -1)

    def _build_graph(self):
        """Build the graph.

        Builds only the nodes that are known, ie. does not build
        anything below evolvers, if the graph is evolving. In such a
        case, creation of the finalizing layer is also postponed,
        until all evolvers are expanded.

        If the graph is not evolving, it is created in one go.
        """

        logger.info('Start neads graph building', 1)
        self.first_layer, loading_last = self.configuration.loading.create(
            self.node_factory)
        if self.is_evolving:
            last_layer = self._build_given_phases(
                self._phases_up_to_evolution, loading_last)
            self._evolvers_to_expand = len(last_layer)
        else:
            last_layer = self._build_given_phases(
                self._developing_phases, loading_last)
            # graph is fully constructed, only finalizers remain
            self.configuration.finalizing.create(self.node_factory,
                                                 last_layer)
        logger.info('End neads graph building', -1)

    def _build_given_phases(self, phases: Iterable[Phase], last_layer):
        """Build given phases and attach them to the given last_layer.

        Phases are built one the bottom of each other. That is,
        the first layer is attached directly to the given last_layer
        and the subsequent phases are always attached to their preceding
        layer.

        Parameters
        ----------
        phases
            Which phases should be created.
        last_layer
            Collection of nodes to which the created layers should be
            attached.

        Returns
        -------
        [Node]
            Bottom most nodes of the last created layer.
        """

        for phase in phases:
            if not phase.empty:
                last_layer = self._create_phase(phase, last_layer)
        return last_layer

    def _create_phase(self, phase: Phase, last_layer: Iterable[Node]):
        """Create the given phase and attach it to the given last_layer.

        The rule is such that a particular phase is always attached to
        one node. Therefore, the phase is created for each node of the
        given last layer.

        Parameters
        ----------
        phase
            Phase to build.
        last_layer
            Collection of nodes to which the created layer should be
            attached.

        Returns
        -------
        [Node]
            Bottom most nodes of the created layer.
        """

        new_last_layer = []
        for node in last_layer:
            initial_nodes, end_nodes = phase.create(self.node_factory)
            node.attach_children(initial_nodes)
            new_last_layer += end_nodes
        return new_last_layer

    def expand_evolver(self, evolver, interval_count):
        """Expand the given evolver, ie. build the rest of its branch.

        Parameters
        ----------
        evolver
            Evolver to expand.
        interval_count
            Number of extractors that will extract the data from evolver.

        Raises
        ------
        NeadsEvolverWasAlreadyExpanded
            If the evolver was already expanded earlier.
        """

        if evolver.expanded:
            raise eh.NeadsEvolverWasAlreadyExpanded(
                f'Given evolver was already expanded: {evolver}'
            )

        evolver.expanded = True
        self._evolvers_to_expand -= 1
        extractors = self.configuration.evolution.expand_evolver(
            evolver,
            interval_count,
            self.node_factory
        )

        last_layer = self._build_given_phases(
            self._phases_after_evolution, extractors)
        self._last_layer_from_expansion.extend(last_layer)

        if not self._evolvers_to_expand:
            self.configuration.finalizing.create(
                self.node_factory,
                self._last_layer_from_expansion
            )

