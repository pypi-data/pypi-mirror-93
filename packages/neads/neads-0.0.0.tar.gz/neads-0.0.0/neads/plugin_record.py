"""Module proving PluginRecord to describe desired plugin activations."""

# TODO: examine whether the PluginType and PhaseType are necessary
#  eg. node can get PluginType as a class of the PluginRecord
#                   PhaseType as a class of a Phase in where was created

# TODO: is 'origin' used anywhere?

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Callable, Optional
from abc import abstractmethod, ABC
from enum import Enum, auto

from neads.plugin_use import PluginUse
import neads.logger as logger

if TYPE_CHECKING:
    from neads.node_factory import NodeFactory
    from neads.referencing_rules import MergeRule, TakeRule
    from neads.nodes import Node


class PluginType(Enum):
    """Type of plugin."""

    LOADER = auto(),
    PREPROCESSOR = auto(),
    EVOLVER = auto(),
    EXTRACTOR = auto(),
    BUILDER = auto(),
    WEIGHTED_EDITOR = auto(),
    FILTER = auto(),
    UNWEIGHTED_EDITOR = auto(),
    ANALYZER = auto(),
    FINALIZER = auto(),


class PhaseType(Enum):
    """Phase in which plugin appears."""

    LOADING = auto(),
    PREPROCESSING = auto(),
    EVOLUTION = auto(),
    BUILDING = auto(),
    WEIGHTED_EDITING = auto(),
    FILTERING = auto(),
    UNWEIGHTED_EDITING = auto(),
    ANALYZING = auto(),
    FINALIZING = auto(),


class PluginRecord(ABC):
    """Description acting plugin and its parameters sets.

    The records information describes the plugin and says with which
    parameters it is supposed to be executed. When there is more
    parameters sets provided

    The plugin is identified by its name and version. They
    identification serves as a key for the data in the `Project`
    database and for searching for the `Plugin` itself, ie. for its
    source code, unless the method is provided directly.

    Note that the results are stored in a database under a key which is
    composed from names, version and params sets of plugins which
    gradually created the data. Therefore, any change of a plugin which
    can cause producing different results when being called with the same
    params set needs to trigger a change of version.

    Attributes
    ----------
    name : str
        Name of the acting plugin.
    params_sets : Iterable[dict]
        Collection of params sets with which the plugin will be
        executed. Each params set is a dictionary which is passed
        to the plugin method as a collection of keyword arguments.

        When more params sets is provided, they are required to have
        the same collection of keys.

        If the method is provided, its parameters must comply with
        given params sets. If the default case, ie. method is not
        provided, the method in the plugin source file is required
        to have complying parameters, as well.

    version : int
        Version of the acting plugin.
    method : Optional[Callable]
        Method of the acting plugin. It need not to be specified,
        in that case plugin method will be obtained from plugin pool
        during computation.

    Notes
    -----
    There exists a subclass of PluginRecord for each phase for some
    historical reasons. They are excessive, the author knows it and will
    remove them at first opportunity.
    """

    def __init__(self, name : str, params_sets: Iterable[dict], *,
                 version: int, method: Optional[Callable] = None):
        """Initialize a PluginRecord instance.

        Parameters
        ----------
        name : str
            Name of the acting plugin.
        params_sets : Iterable[dict]
            Collection of params sets with which the plugin will be
            executed. Each params set is a dictionary which is passed
            to the plugin method as a collection of keyword arguments.

            When more params sets is provided, they are required to have
            the same collection of keys.

            If the method is provided, its parameters must comply with
            given params sets. If the default case, ie. method is not
            provided, the method in the plugin source file is required
            to have complying parameters, as well.

        version : int
            Version of the acting plugin.
        method : Optional[Callable]
            Method of the acting plugin. It need not to be specified,
            in that case plugin method will be obtained from plugin pool
            during computation.
        """

        self.name = name
        self.params_sets = params_sets
        self.version = version
        self.method = method

    # TODO: rename.. create is just not enough
    # TODO: why it creates directly the nodes?
    def create(self, node_factory: NodeFactory) -> [Node]:
        """Create a list of nodes, one for each params set of the record.

        Parameters
        ----------
        node_factory
            Factory for creating nodes.

        Returns
        -------
        [Node]
            List of nodes with plugins corresponding to the record's
            plugin. Each one of them has one params set of the record
            and they are in the order corresponding to the order of
            params sets. None of the nodes has any parent or child.
        """

        factory = self._select_factory_method(node_factory)
        nodes = []
        for params in self.params_sets:
            plugin_use = PluginUse(self, params)
            nodes.append(factory(plugin_use))
            logger.info(f'Created {nodes[-1]}', 0)
        return nodes

    @abstractmethod
    def _select_factory_method(self, node_factory: NodeFactory):
        """Select the right method from the given factory."""
        pass

    @property
    @abstractmethod
    def plugin_type(self) -> PluginType:
        """Return type of the plugin."""
        pass

    @property
    @abstractmethod
    def phase_type(self) -> PhaseType:
        """Return type in which the plugin appears."""
        pass

    @property
    def origin(self):
        """Return identification number of the record."""
        # TODO: is this necessary?
        # Unifying with plugin_uses for easier work with ref rules
        return id(self)


class LoaderRecord(PluginRecord):
    def _select_factory_method(self, node_factory):
        """Select the right method from the given factory."""
        return node_factory.create_loader

    @property
    def plugin_type(self):
        """Return PluginType.LOADER."""
        return PluginType.LOADER

    @property
    def phase_type(self):
        """Return PhaseType.LOADING."""
        return PhaseType.LOADING


class PreprocessorRecord(PluginRecord):
    def _select_factory_method(self, node_factory):
        """Select the right method from the given factory."""
        return node_factory.create_preprocessor

    @property
    def plugin_type(self):
        """Return PluginType.PREPROCESSOR."""
        return PluginType.PREPROCESSOR

    @property
    def phase_type(self):
        """Return PhaseType.PREPROCESSING."""
        return PhaseType.PREPROCESSING


class EvolverRecord(PluginRecord):
    def _select_factory_method(self, node_factory):
        """Select the right method from the given factory."""
        return node_factory.create_evolver

    @property
    def plugin_type(self):
        """Return PluginType.EVOLVER."""
        return PluginType.EVOLVER

    @property
    def phase_type(self):
        """Return PhaseType.EVOLUTION."""
        return PhaseType.EVOLUTION


class ExtractorRecord(PluginRecord):
    def _select_factory_method(self, node_factory):
        """Select the right method from the given factory."""
        return node_factory.create_extractor

    @property
    def plugin_type(self):
        """Return PluginType.EXTRACTOR."""
        return PluginType.EXTRACTOR

    @property
    def phase_type(self):
        """Return PhaseType.EVOLUTION."""
        return PhaseType.EVOLUTION


class BuilderRecord(PluginRecord):
    def _select_factory_method(self, node_factory):
        """Select the right method from the given factory."""
        return node_factory.create_builder

    @property
    def plugin_type(self):
        """Return PluginType.BUILDER."""
        return PluginType.BUILDER

    @property
    def phase_type(self):
        """Return PhaseType.BUILDING."""
        return PhaseType.BUILDING


class WeightedEditorRecord(PluginRecord):
    def _select_factory_method(self, node_factory):
        """Select the right method from the given factory."""
        return node_factory.create_weighted_editor

    @property
    def plugin_type(self):
        """Return PluginType.WEIGHTED_EDITOR."""
        return PluginType.WEIGHTED_EDITOR

    @property
    def phase_type(self):
        """Return PhaseType.WEIGHTED_EDITING."""
        return PhaseType.WEIGHTED_EDITING


class FilterRecord(PluginRecord):
    def _select_factory_method(self, node_factory):
        """Select the right method from the given factory."""
        return node_factory.create_filter

    @property
    def plugin_type(self):
        """Return PluginType.FILTER."""
        return PluginType.FILTER

    @property
    def phase_type(self):
        """Return PhaseType.FILTERING."""
        return PhaseType.FILTERING


class UnweightedEditorRecord(PluginRecord):
    def _select_factory_method(self, node_factory):
        """Select the right method from the given factory."""
        return node_factory.create_unweighted_editor

    @property
    def plugin_type(self):
        """Return PluginType.UNWEIGHTED_EDITOR."""
        return PluginType.UNWEIGHTED_EDITOR

    @property
    def phase_type(self):
        """Return PhaseType.UNWEIGHTED_EDITING."""
        return PhaseType.UNWEIGHTED_EDITING


class AnalyzerRecord(PluginRecord):
    def _select_factory_method(self, node_factory):
        """Select the right method from the given factory."""
        return node_factory.create_analyzer

    @property
    def plugin_type(self):
        """Return PluginType.ANALYZER."""
        return PluginType.ANALYZER

    @property
    def phase_type(self):
        """Return PhaseType.ANALYZING."""
        return PhaseType.ANALYZING


class FinalizerRecord(PluginRecord):
    """Description finalizer plugin and its parameters sets.

    FinalizerRecords are standard PluginRecords extended with two extra
    parameters which is `merge_rule` and `take_rule`. They serve for
    referencing other plugin activations involved in the computation
    process.

    Attributes
    ----------
    merge_rules : Iterable[MergeRule]
        Rules which select the sets of plugins which is possible to
        reference via take_rules.
    take_rules: Iterable[TakeRule]
        Rules which creates a reference from the finalizer to nodes
        which comply with the rule which are from a group of node
        according to the merge_rules.
    """

    def __init__(self, name, params_sets, *, version, method=None,
                 merge_rules: Iterable[MergeRule],
                 take_rules: Iterable[TakeRule]):
        """Initialize a PluginRecord instance.

        Parameters
        ----------
        name
            Name of the acting plugin.
        params_sets
            Collection of params sets with which the plugin will be
            activated.
        version
            Version of the acting plugin.
        method
            Method of the acting plugin. It need not to be specified,
            in that case plugin method will be obtained from plugin pool
            during computation.
        merge_rules
            Collection of rules that specify the sets of nodes from
            which the finalizers will be able to take their data.
        take_rules
            Collection of rules that directly specify from which nodes
            the finalizers take their data.
        """

        super().__init__(name, params_sets, version=version, method=method)
        self.merge_rules = merge_rules
        self.take_rules = take_rules

    def _select_factory_method(self, node_factory):
        """Select the right method from the given factory."""
        return node_factory.create_finalizer

    @property
    def plugin_type(self):
        """Return PluginType.FINALIZER."""
        return PluginType.FINALIZER

    @property
    def phase_type(self):
        """Return PhaseType.FINALIZING."""
        return PhaseType.FINALIZING
