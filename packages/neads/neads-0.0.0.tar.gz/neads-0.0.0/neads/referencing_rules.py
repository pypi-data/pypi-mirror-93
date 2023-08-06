"""Module providing tools for referencing nodes in computation graph.

There are two main reasons for referencing, as the names TakeRule and
MergeRule suggest. We want to either reference some nodes, because we
can get their data or we want to affect the merging algorithm for
creation of finalizers. See the mentioned classes for more details.
"""
# TODO: think through whether at it sufficient that the rule applies to
#  node
#  It will become a problem, when more complex phases arrive

from __future__ import annotations

from typing import Union
from abc import ABC, abstractmethod
from neads.nodes import Node
from neads.plugin_record import PluginRecord
from neads.plugin_use import PluginUse

from neads.plugin_record import PluginType


class MergeRule(ABC):
    """Tool for specifying which branches should be considered equal.

    MergeRules play important role in merging algorithm, which decides
    how many finalizers will be created and from which branches will
    come their data.

    The main principle is that one finalizer is created for each
    equivalence class of branches. In default setting, no two branches
    are equivalent, as they differ in at least one plugin. Hence,
    one finalizer is created at the bottom of each branch.

    However, by passing a merge rule, the algorithm gets information
    that a particular difference between branches should be ignored.
    Therefore, some branches may become equivalent and only one common
    finalizer will be created for all of them.
    """

    @abstractmethod
    def applies_to(self, reference_target: Node) -> bool:
        """Return whether it applies to the given node.

        The meaning of "rule applies to node" is that the difference in
        the particular node should be ignored in the merging algorithm.

        Parameters
        ----------
        reference_target : Node
            Node to be tested, whether the rule applies to it.

        Returns
        -------
        bool
            Result of test, whether the rule applies to the given node.
        """

        pass


class TakeRule(ABC):
    """Tool for specifying nodes that will pass their data to finalizer.

    Each finalizer is created at the bottom of a certain set of
    branches. TakeRules are the way how to say, which data should the
    finalizer get from those branches. It gets data from exactly those
    nodes for which applies at least one of the given take rules.
    """

    @abstractmethod
    def applies_to(self, reference_target: Node) -> bool:
        """Return whether it applies to the given node.

        When rule applies to node, the data produced by the targeted node
        will be passed to the corresponding finalizer.

        Parameters
        ----------
        reference_target : Node
            Node to be tested, whether the rule applies to it.

        Returns
        -------
        bool
            Result of test, whether the rule applies to the given node.
        """

        pass


class IndividualReferenceRule(MergeRule, TakeRule):
    """Reference rule aiming individual PluginRecord instead of phases.

    Each of these reference rules is bound to particular PluginRecord
    and it applies only for nodes that originate from the PluginRecord.

    Individual reference rules can target only plugins from alteration
    phases to preserve symmetry in merging and/or taking.

    Attributes
    ----------
    IndividualReferenceRule.allowed_types : [PluginType]
        Collection of all plugin types of valid PluginRecord to be
        referenced.

        Allowed types are PREPROCESSOR, WEIGHTED_EDITOR,
        UNWEIGHTED_EDITOR and FINALIZER.
    """

    allowed_types = [
        PluginType.PREPROCESSOR,
        PluginType.WEIGHTED_EDITOR,
        PluginType.UNWEIGHTED_EDITOR,
        PluginType.FINALIZER
    ]

    def __init__(self, plugin_record: PluginRecord):
        """Initialize the instance with targeted PluginRecord.

        Parameters
        ----------
        plugin_record : PluginRecord
            PluginRecord whose corresponding nodes will be targeted,
            ie. the rule applies only for those node, which originate
            from the given PluginRecord.
        """
        if plugin_record.plugin_type in self.allowed_types:
            self.plugin_record = plugin_record
        else:
            raise ValueError(f'Invalid plugin type of given record for '
                             f'individual referencing: {plugin_record}')

    def applies_to(self,
                   reference_target: Union[Node, PluginUse, PluginRecord])\
            -> bool:
        """Return whether it applies to the given node.

        It applies iff PluginRecord of the given node, ie. its origin,
        is the same as the one with which the rule was initialized.

        Parameters
        ----------
        reference_target : Node
            Node to be tested, whether the rule applies to it.

        Returns
        -------
        bool
            Result of test, whether the rule applies to the given node.
        """

        if isinstance(reference_target, PluginUse):
            return self.plugin_record.origin == reference_target.origin
        elif isinstance(reference_target, Node):
            return self.plugin_record.origin == \
                   reference_target.plugin_use.origin
        elif isinstance(reference_target, PluginRecord):
            return self.plugin_record.origin == reference_target.origin
        else:
            raise ValueError(reference_target)


class NonIndividualReferenceRule(MergeRule, TakeRule):
    """Reference rule aiming phases instead of individual PluginRecords.

    These rules are not bound to particular PluginRecords unlike
    IndividualReferenceRules. They reference all the nodes having a
    specific type.

    Attributes
    ----------
    NonIndividualReferenceRule.allowed_types : [PluginType]
        Collection of all valid plugin types which can be referenced.

        Allowed types are LOADER, EXTRACTOR, BUILDER, FILTER and ANALYZER.

        For merging by intervals of evolution, use PluginType.EXTRACTOR.
    """
    # TODO: expect referencing not just to a single nodes, but actually
    #  the whole phases (with allowing the transformation phases be more
    #  complex)

    allowed_types = [
        PluginType.LOADER,
        PluginType.EXTRACTOR,
        PluginType.BUILDER,
        PluginType.FILTER,
        PluginType.ANALYZER
    ]

    def __init__(self, plugin_type: PluginType):
        """Initialize the instance with targeted PluginRecord.

        Parameters
        ----------
        plugin_type : PluginType
            PluginType whose corresponding nodes will be targeted,
            ie. the rule applies only for those node, which have the
            given plugin type.
        """
        if plugin_type in self.allowed_types:
            self.plugin_type = plugin_type
        else:
            raise ValueError(f'Invalid plugin type for '
                             f'non-individual referencing: {plugin_type}')

    def applies_to(self, reference_target: Union[Node, PluginRecord]) -> \
            bool:
        """Return whether it applies to the given node.

        It applies iff PluginType of the given node, is the same as the
        one with which the rule was initialized.

        Parameters
        ----------
        reference_target : Node
            Node to be tested, whether the rule applies to it.

        Returns
        -------
        bool
            Result of test, whether the rule applies to the given node.
        """

        # TODO: delete this "Union[Node, PluginRecord]" nonsense
        #  one type must be enough
        if isinstance(reference_target, Node):
            given_type = reference_target.plugin_use.plugin_type
        # add PluginUse as an option
        else:
            given_type = reference_target.plugin_type
        return given_type == self.plugin_type
