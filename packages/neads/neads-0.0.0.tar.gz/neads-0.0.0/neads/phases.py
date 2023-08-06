"""Module providing phases.

Phase is a common base class for all phases. SequencePhase and
TransformationPhase are two abstract subclasses implementing common
behaviour for many concrete phase classes.
"""

# TODO: check, whether a SequencePhase can be initialized

# TODO: why Finalizing is not a Phase?

# TODO: consider better naming convention
#  eg. plugin is not great for plugin_record

# TODO: consider move loader to TransformationPhases

# TODO: add layer for gathering the data assembly / collection /
#  accumulation?

from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Iterable, Optional
from collections import defaultdict
from abc import ABC, abstractmethod
from itertools import product

from neads.plugin_record import ExtractorRecord, FinalizerRecord
from neads.branch_merger import BranchMerger, BranchSet
from neads.phase_log_mixin import PhaseLogMixin
from neads.plugin_record import PluginRecord

if TYPE_CHECKING:
    from neads.nodes import Node
    from neads.node_factory import NodeFactory
    from neads.plugin_record import LoaderRecord, \
        EvolverRecord


class Phase(PhaseLogMixin, ABC):
    """Common base class for all phases."""

    @abstractmethod
    def create(self, node_factory: NodeFactory) \
            -> Tuple[Iterable[Node], Iterable[Node]]:
        """Create a part of graph corresponding to the phase.

        Parameters
        ----------
        node_factory
            Factory for creating graph nodes.

        Returns
        -------
        Tuple[Iterable[Node], Iterable[Node]]
            The first item in tuple is a collection of top most nodes of
            the phase. They should be attached to the preceding phase.
            The second item is a collection of top most nodes of the
            phase. The succeeding phase should be attached to them.
        """

        pass

    @property
    @abstractmethod
    def empty(self) -> bool:
        """Return whether there is any plugin action in the phase."""
        pass


class AlterationPhase(Phase, ABC):
    """Base class for all alteration phases.

    Alteration phases consist of a sequence of plugins which are evaluated
    gradually, one by one, and there are expected to produce the same
    type of data as they received.
    """

    def __init__(self, *alterators: PluginRecord):
        """Initialize an AlterationPhase.

        Parameters
        ----------
        alterators : PluginRecord
            A sequence of PluginRecords describing the gradual actions of
            the phase.
        """

        self.alterators = alterators

    def create(self, node_factory: NodeFactory):
        """Create a part of graph corresponding to the phase.

        Nodes of PluginRecords are organized in layers by their order
        in the phase. In the first layer, there are nodes of the first
        PluginRecord, while in the last layer, there are nodes of the last
        PluginRecord.

        Branches are created in expected way, ie. if a particular
        PluginRecord produces more nodes, under each of them will be
        built the remaining layers.

        Parameters
        ----------
        node_factory
            Factory for creating graph nodes.

        Returns
        -------
        Tuple[Iterable[Node], Iterable[Node]]
            First item in tuple is a collection of top most nodes of the
            phase. They should be attached to the preceding phase.
            The second argument is a collection of top most nodes of the
            phase. The succeeding phase should be attached to them.
        """

        self._log_start_creating_layer()
        first_layer = self.alterators[0].create(node_factory)
        last_layer = first_layer
        for idx in range(1, len(self.alterators)):
            plugin = self.alterators[idx]
            # TODO: consider extracting this cycle to own method
            new_last_layer = []
            for node in last_layer:
                new_nodes = plugin.create(node_factory)
                node.attach_children(new_nodes)
                new_last_layer.extend(new_nodes)
            last_layer = new_last_layer
        self._log_end_creating_layer()
        return first_layer, last_layer

    @property
    def empty(self):
        """Return whether there is any plugin action in the phase."""
        return not bool(self.alterators)


class TransformationPhase(Phase, ABC):
    """Base class for all transformation phases.

    Transformation phases consist of a collection of plugins which are
    evaluated in parallel. That is, they do not cooperate with each other,
    each of them just gets its data and the produced result is send to
    a layer belonging to succeeding phase.
    """

    def __init__(self,
                 *transformers: PluginRecord):
        """Initialize a TransformationPhase.

        Parameters
        ----------
        transformers : PluginRecord
            A collection of PluginRecords describing the actions of
            the phase.
        """

        self.transformers = transformers

    def create(self, node_factory: NodeFactory):
        """Create a part of graph corresponding to the phase.

        Nodes of PluginRecords form just a one layer. Each node
        correspond to one params set of one of the transformers.

        Parameters
        ----------
        node_factory
            Factory for creating graph nodes.

        Returns
        -------
        Tuple[Iterable[Node], Iterable[Node]]
            First item in tuple is a collection of top most nodes of the
            phase and the second argument is a collection of top most
            nodes of the phase.

            But as only one layer of nodes is produced, the layer is
            returned in the two items.
        """

        self._log_start_creating_layer()
        transformers_sets = [plugin.create(node_factory)
                             for plugin in self.transformers]
        flat = [t for tr_set in transformers_sets for t in tr_set]
        self._log_end_creating_layer()
        return flat, flat

    @property
    def empty(self):
        """Return whether there is any plugin action in the phase."""
        return not bool(self.transformers)


class Loading(TransformationPhase):
    """Phase for loading the initial time series."""
    pass


class Preprocessing(AlterationPhase):
    """Phase for preprocessing the time series."""

    pass


class Evolution(Phase):
    """Phase for division the time series into overlapping intervals.

    If an evolver is provided, it produces a box with only one node.
    However, after the node is evaluated (and it is always evaluated),
    more nodes will be created. One for each interval of evolution.

    The new nodes are called extractors, as they extract the data from
    source of evolver **by instruction** from evolver. That is, evolver
    says how many intervals there will be, and what are their boundaries.

    The extractors are the outputs of the phase. Their number is
    determined by the evolver which also heavily depends on its input data.

    The process of creating extractor nodes and rest of the subtree
    under the particular branch with the evolution phase is called
    *evolver expansion*.
    """

    def __init__(self, evolver: Optional[EvolverRecord] = None):
        """Initialize an Evolving phase.

        Parameters
        ----------
        evolver : EvolverRecord
            EvolverRecord describing the evolver plugin and its params.
        """

        # TODO: what would happen if we would allow more evolvers?
        #  or evolver with multiple params?
        self.evolver = evolver

    def create(self, node_factory: NodeFactory):
        """Create a part of graph corresponding to the phase.

        There is a restriction which implies that there can be only one
        evolver node in the evolving phase.

        Parameters
        ----------
        node_factory
            Factory for creating graph nodes.

        Returns
        -------
        Tuple[Iterable[Node], Iterable[Node]]
            Only one evolver node is created and it is returned as a
            single item of a list. The list is returned twice to comply
            with general 'create' method.
        """

        self._log_start_creating_layer()
        # As all plugin records, list of nodes is returned
        # But the evolvers is allowed to have only one params set
        evolver_in_list = self.evolver.create(node_factory)
        self._log_end_creating_layer()
        return evolver_in_list, evolver_in_list

    @property
    def empty(self):
        """Return whether there is any plugin action in the phase."""
        return not bool(self.evolver)

    @staticmethod
    def expand_evolver(evolver_node: Node, interval_count, node_factory):
        """Create layer of extractors attached to the given evolver.

        Parameters
        ----------
        evolver_node
            The expanded evolver.
        interval_count
            Number of intervals produced by the evolver, which
            determines the number of created extractors.
        node_factory
            Factory for creating the extractor nodes.

        Returns
        -------
        Iterable[Node]
            Collection of created extractors.
        """

        extractor_record = Evolution._create_extractor_record(
            interval_count)
        extractors = extractor_record.create(node_factory)
        evolver_node.attach_children(extractors)  # evolver
        evolver_node.parents[0].attach_children(extractors)  # series
        return extractors

    @staticmethod
    def _create_extractor_record(interval_count):
        """Create extractor record with params set for each interval.

        Parameters
        ----------
        interval_count : int
            Says how many intervals is there to extract. The returned
            record has one params set for each interval.

        Returns
        -------
        ExtractorRecord
            ExtractorRecord with name 'extractor', params sets
            'interval' with numbers from 0 to interval_count - 1 and
            version 0.
        """

        # TODO: consider lambda instead of file
        return ExtractorRecord(
            'extractor',
            [{'interval': interval} for interval in range(interval_count)],
            version=0,
            method=Evolution._extractor_method
        )

    @staticmethod
    def _extractor_method(data, interval):
        ddf, d = data[0]  # evolver data
        intervals = d['data']
        ddf, d = data[1]  # time series
        df = d['data']
        start, end = intervals[interval]
        return {'data': df.iloc[start:end, :]}


class Building(TransformationPhase):
    """Phase for creating weighted networks from given time series."""
    pass


class WeightedEditing(AlterationPhase):
    """Phase for modification of weighted networks."""
    pass


class Filtering(TransformationPhase):
    """Phase for creating unweighted networks from weighted networks."""
    pass


class UnweightedEditing(AlterationPhase):
    """Phase for modification of unweighted networks."""
    pass


class Analyzing(TransformationPhase):
    """Phase for calculation of particular network characteristics."""
    pass


# TODO: finalizing will probably need a heavy refactorization
#  it is an absolute mess

class Finalizing(PhaseLogMixin):
    """Phase for collecting data and producing final results.

    The number of created finalizer nodes depends on the shape of the
    preceding phases and parameters *merge_rules* and *take_rules* of
    individual finalizers.

    Merge rules of each finalizer divide the nodes of the bottom most
    layer of the tree into groups. For each group, one finalizer node is
    created. Take rules parameters decide, which ancestors of the nodes
    from the group will provide their data to the finalizer node.

    Succeeding finalizer always inherits merge rules of its predecessors,
    i.e. the number of groups may only decrease by adding a new rule,
    but never increases.
    """

    def __init__(self, *finalizers: FinalizerRecord):
        """Initialize a Finalizing phase.

        Parameters
        ----------
        finalizers : FinalizerRecord
            Sequence of FinalizerRecords describing the how the data
            accumulation should be organized and which data should be
            actually extract from the graph.
        """

        self.finalizers = finalizers

    def create(self, node_factory: NodeFactory, last_layer: [Node]):
        """Create the finalizing phase.

        Parameters
        ----------
        node_factory
            Factory for creating the extractor nodes.
        last_layer
            Bottom most layer of the graph.
        """

        # TODO: consider { FinalizerRecord : { BranchSet: [Nodes] } }
        #  for the created layers + relation on BranchSets
        #  it would be faster, but mainly better explain the algorithm
        self._log_start_creating_layer()
        # Serves for correct referencing among finalizers
        # { FinalizerRecord: { Leaf: FinalizerNode } }
        created_layers = defaultdict(dict)
        merger = BranchMerger(last_layer)
        for finalizer in self.finalizers:
            merger.merge(finalizer.merge_rules)
            # TODO: consider extracting this cycle to own method
            for branch_set in merger.branch_partition:
                new_node = self._create_node_for_set(finalizer,
                                                     branch_set,
                                                     created_layers,
                                                     node_factory)
                self._update_created_layers(finalizer,
                                            new_node,
                                            branch_set,
                                            created_layers)
        self._log_end_creating_layer()
        # TODO: consider returning something

    def _create_node_for_set(self,
                             finalizer: FinalizerRecord,
                             branch_set: BranchSet,
                             created_layers,
                             node_factory: NodeFactory):
        """Create finalizer node for given equivalence set of branches.

        Parameters
        ----------
        finalizer : FinalizerRecord
            Prescription of properties of the created node.
        branch_set : BranchSet
            Equivalence class of branches for which the finalizer will
            be created.
        created_layers
            Object containing description of created layers which will
            be used to determine parent of created node among finalizers.
        node_factory
            Factory for creating the extractor nodes.

        Returns
        -------
        Node
            Created node.
        """

        # TODO: parents of the node can be passed directly
        #  this way the very complicated structure 'created_layers'
        #  spans two more methods than needed
        new_node = finalizer.create(node_factory)[0]  # returns list
        self._add_references_along_branches(finalizer, new_node,
                                            branch_set)
        self._add_references_to_previous_finalizers(finalizer,
                                                    new_node,
                                                    branch_set,
                                                    created_layers)
        return new_node

    def _add_references_along_branches(self, finalizer: FinalizerRecord,
                                       new_node: Node,
                                       branch_set: BranchSet):
        """Add references to non-finalizer nodes.

        Parameters
        ----------
        finalizer : FinalizerRecord
            Finalizer record with TakeRules, which determines nodes to
            be referenced.
        new_node
            The created node whose references will be added.
        branch_set
            Equivalence class of branches on which nodes the finalizer
            will reference.
        """

        parents = branch_set.take(finalizer.take_rules)
        for parent in parents:
            parent.attach_children([new_node])

    def _add_references_to_previous_finalizers(self,
                                               finalizer: FinalizerRecord,
                                               new_node: Node,
                                               branch_set: BranchSet,
                                               created_layers):
        """Add references to finalizer nodes of previous FinalizerRecords.

        Parameters
        ----------
        finalizer : FinalizerRecord
            Finalizer record with TakeRules, which determines nodes to
            be referenced.
        new_node
            The created node whose references will be added.
        branch_set
            Equivalence class of branches. The new node will reference
            those finalizer nodes with which it shares leaves, ie. they
            both are attached under the same branch.
        created_layers
            Object containing description of created layers which will
            be used to determine parent of created node among finalizers.
        """

        for previous_finalizer, take_rule in product(created_layers,
                                                     finalizer.take_rules):
            if take_rule.applies_to(previous_finalizer):
                # { Leaf: FinalizerNode }
                target_layer = created_layers[previous_finalizer]
                # We have the right layer of finalizer nodes
                # finalizer_node will reference to those nodes which are
                # underneath its leaf, ie. the share leaves
                leaves = [leaf_1 for leaf_1, leaf_2
                          in product(branch_set.leaves, target_layer)
                          if leaf_1 is leaf_2]
                finalizer_nodes = [target_layer[leaf] for leaf in leaves]
                non_duplicate_nodes = list(dict.fromkeys(finalizer_nodes))
                for node in non_duplicate_nodes:
                    node.attach_children(new_node)

    def _update_created_layers(self, finalizer: FinalizerRecord,
                               new_node: Node, branch_set: BranchSet,
                               created_layers):
        """Update created_layers object after addition of new node."""
        for leaf in branch_set.leaves:
            created_layers[finalizer][leaf] = new_node

    @property
    def empty(self):
        """Return whether there is any plugin action in the phase."""
        return not bool(self.finalizers)
