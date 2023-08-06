"""Module providing support for algorithm creating the finalizers.

Class BranchMerger is central in this process. The indented use is the
following: a BranchMerger instance is created with all leaves of the
graph. Then there will be alternation of two action. First, new merge
rules are passed to the instance via merge method, which changes the
structure of equivalence classes of branches. Second, from each BranchSet
(an equivalence class) are taken nodes on which the particular finalizer
references. See documentation of both classes for more detail.
"""
# TODO: create Branch as a type
# TODO: create Equivalence relation as a type
#  (performed by merge rules)


from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Set
from itertools import chain

if TYPE_CHECKING:
    from neads.nodes import Node
    from neads.referencing_rules import MergeRule, TakeRule


class BranchSet:
    """Represent an equivalence class of branches under some merge rules.

    The class is a helper for branch merging algorithm. As said, branches
    of one equivalence are stored in one BranchSet. Usually
    implementation of some methods (for example is_similar) relies on
    this fact. See their documentation for more detail.

    The main purpose of BranchSet is to provide the user of branch_merger
    module method take. The method extracts nodes on which user points by
    the given take rules.

    Attributes
    ----------
    leaves : Iterable[Node]
        Collection of leaves of branches of the BranchMerger.
    """

    def __init__(self, leaves: Iterable[Node]):
        """Initialize BranchSet with leaves of similar branches.

        Parameters
        ----------
        leaves
            Collection of leaves of similar branches.
        """

        self.leaves = leaves

    def take(self, take_rules: Iterable[TakeRule]) -> Set[Node]:
        """Returns a set of nodes from held branches satisfying given rule.

        Each node from each branch is tested whether it satisfies given
        rules. The method returns a set of those nodes which satisfy at
        least one rule.

        Parameters
        ----------
        take_rules
            Collection of TakeRules that determines which nodes from
            given branches will be returned.

        Returns
        -------
        Set[Node]
            A set of nodes that satisfy at least one of given rules.
        """

        visited = set()
        to_take = set()
        self._dfs_recursion(self.leaves, take_rules, visited, to_take)
        return to_take

    def _dfs_visit_node(self, node, take_rules, visited, to_take):
        """Visit and test a given node and recursively its parents.

        The given node is added to visited set

        Parameters
        ----------
        node
            Node that is visited and tested. It is added to visited set
            and also to to_take set, if satisfies at least one take_rule.
        take_rules
            Collection of TakeRules that determines which nodes from
            given branches will be returned.
        visited
            Set of already visited nodes.
        to_take
            Set of visited nodes which satisfy at least one take rule.
        """

        visited.add(node)
        if any([rule.applies_to(node) for rule in take_rules]):
            to_take.add(node)
        self._dfs_recursion(node.parents, take_rules, visited, to_take)

    def _dfs_recursion(self, nodes_to_visit, take_rules, visited, to_take):
        """Start new dfs recursion activation for given nodes.

        Call _dfs_visit_node for those given nodes which will be
        unvisited at the time of the dfs-call.

        Note that a node may be unvisited when this method is called but
        may be visited during visiting of preceding nodes in
        nodes_to_visit. Then the mention method is not called.

        Parameters
        ----------
        nodes_to_visit
            Nodes to be visited, but only those which were not visited
            yet may be visited.
        take_rules
            Collection of TakeRules that determines which nodes from
            given branches will be returned.
        visited
            Set of already visited nodes.
        to_take
            Set of visited nodes which satisfy at least one take rule.
        """

        for node in nodes_to_visit:
            if node not in visited:
                self._dfs_visit_node(node, take_rules, visited, to_take)

    def is_similar(self, other: BranchSet,
                   merge_rules: Iterable[MergeRule]) -> bool:
        """Test similarity of given BranchSet to self under given rules.

        It is assumed that given collection of rules is a super set of a
        collection of rules under whose the branches in self and in the
        other are similar.

        The consequence of this assumption is that the given merge rules
        define an equivalence relation whose equivalence classes arise
        from sets of the previous equivalence relation, ie. the one that
        grouped together the branches in self and other BranchSets.

        Parameters
        ----------
        other
            The other BranchesSet to be compared with self.
        merge_rules
            Collection of rules under which the similarity is tested.

        Returns
        -------
        bool
            True, if given BranchSet is similar to self under given set of
            merge rules.
        """
        # TODO: very arbitrary cascade of methods purely created for
        #  purpose of serving BranchMerger in a quite specific
        #  algorithm.. it need to be more self-contained with error checks

        # TODO: fix similarity check so that we needn't assume weird
        #  equivalence assumption (maybe store merge rules in init under
        #  which they are equivalent and here check that you've got a
        #  superset)

        self_model_leaf = next(iter(self.leaves))
        other_model_leaf = next(iter(other.leaves))
        return self._are_branches_similar(self_model_leaf,
                                          other_model_leaf,
                                          merge_rules)

    def _are_branches_similar(self,
                              node_1: Node, node_2: Node,
                              merge_rules: Iterable[MergeRule]) -> bool:
        """Test similarity of branches of given nodes under a set of rules.

        It is assumed that both nodes have the same depth. Otherwise an
        undefined behavior may arise.

        Parameters
        ----------
        node_1
            First of the nodes to be tested with the second one.
        node_2
            Second of the nodes to be tested with the first one.
        merge_rules
            Collection of rules under which the similarity is tested.

        Returns
        -------
        bool
            True, if the branches are similar. That is all pairs nodes
            along branches are either the same or their difference is
            forgiven by one of the given rules. Otherwise False.
        """
        # TODO: fix so that UB is not a result

        # We can take advantage of very specific shape of branches in
        # the graph.
        # Each leaf is at the same depth and and their parents
        # correspond to the same plugin_records.
        if self._do_nodes_correspond(node_1, node_2, merge_rules):
            for p_1, p_2 in zip(node_1.parents, node_2.parents):
                if not self._are_branches_similar(p_1, p_2,
                                                  merge_rules):
                    return False
            else:
                return True
        else:
            return False

    def _do_nodes_correspond(self,
                             node_1: Node, node_2: Node,
                             merge_rules: Iterable[MergeRule]) -> bool:
        """Test correspondence of two nodes under the given set of rules.

        Parameters
        ----------
        node_1
            First of the nodes to be tested with the second one.
        node_2
            Second of the nodes to be tested with the first one.
        merge_rules
            Collection of rules under which the similarity is tested.

        Returns
        -------
        bool
            If PluginUses of both vertices are the same, or at least one
            rule applies to both vertices.

        Notes
        -----
            It follows from the set of possible rules and expected use
            of this method (ie. for construction finalizers) that the
            given nodes are always from the same depth and usually have
            the same plugin (with exception of transformation phases).
            Hence we may we asserted in the code that exactly the same
            rules applies for both nodes.
        """

        # TODO: fix call with plugin use instead of node
        eval_rules_1 = [rule.applies_to(node_1.plugin_use)
                        for rule in merge_rules]
        eval_rules_2 = [rule.applies_to(node_2.plugin_use)
                        for rule in merge_rules]
        # Checks that the same rules applies on both nodes
        assert all([b_1 == b_2
                    for b_1, b_2 in zip(eval_rules_1, eval_rules_2)])
        return any(eval_rules_1) \
            or node_1.get_data_definition_component() \
            == node_2.get_data_definition_component()

    @staticmethod
    def from_sets(sets: Iterable[BranchSet]) -> BranchSet:
        # TODO: remove this very, very arbitrary method;
        #  use proper constructor instead
        return BranchSet(list(chain(*[set_.leaves for set_ in sets])))


class BranchMerger:
    """Class performing the algorithm of merging branches under some rules.

    BranchMerger represents an algorithm of merging branches by a
    specified set of rules called merge rules. Branch merging means
    grouping together similar graph branches to form a BranchSet, where
    "similarity" relation is defined by received collection of merge rules.
    It is used for creating finalizer's layer.

    By default, a branch is similar only to itself, ie. it is different
    from any other branch, because they differ in at least one node.
    However, a particular difference between branches will become
    ignored by after passing a suitable merge rule via merge method.
    Branches become similar, when all their differences are left out.
    Mathematically speaking, similarity relation is an equivalence.

    For example, let us have two branches that differs in a preprocessor
    plugin and builder plugin. They are not similar. They become similar
    only in such a case when merge rules for both these nodes are provided.

    Branch merging is a gradual process, ie. merging is being done in
    multiple steps (by repeatedly calling the merge method). In each
    step, new merge rules are added, while the previously passed rules
    remains valid. This ensures that the groups of branches (BranchSets)
    across these steps form a hierarchy, ie. if two branches are
    similar, they will remain.

    Attributes
    ----------
    branch_partition : Iterable[BranchSet]
        Collection of current state of branch groups. It is updated
        after each call of merge method. Initially, each group contains
        a single branch.
    _merge_rules : Iterable[MergeRule]
        Collection of all so far received merge rules. It is updated
        after each call of merge method. Initially, it is empty.
    """

    def __init__(self, leaves: Iterable[Node]):
        """Initialize a branch merger with leaves of branches.

        After initialization, each BranchSet consist of a single branch.
        Conversely, for each branch these is a BranchSet.

        Parameters
        ----------
        leaves
            Collection of leaves of branches to be merged. Branch is the
            path (not precise) that leads from a leave to top most layer.

            Leaves must be in equal depth for correct results of the
            algorithm. Otherwise, undefined behavior arise.
        """
        # TODO: branch is not a path
        # TODO: fix (remove) requirement that leaves must have equal
        #  depth; then remove UB

        self.branch_partition = [BranchSet([leave]) for leave in leaves]
        self._merge_rules: [MergeRule] = []

    def merge(self, merge_rules: Iterable[MergeRule]):
        """Perform new merging step by adding new merge rules.

        As the set of all merge rules is extended by given rules,
        similarity relation between branches is redefined. Hence,
        new BranchSets are generated.

        See BranchMerger docstring for details on the exact algorithm.

        Parameters
        ----------
        merge_rules : Iterable[MergeRules]
            Collection of new merge rules to adapt the similarity relation.
        """

        self._merge_rules.extend(merge_rules)
        self.branch_partition = self._get_new_partition()

    def _get_new_partition(self) -> [BranchSet]:
        """Return new partition for current similarity relation.

        Current similarity relation is determined by current set of
        merge rules in attribute _merge_rules.

        Returns
        -------
            New collection of branch sets. Branches sets are determined
            by current similarity relation.
        """

        # Create a refined partition, ie. sets of current classes
        # Then convert it
        refined_partition = {}  # { ModelBranchSet: [EquivalentSets] }
        for branch_set in self.branch_partition:
            for model_branch_set in refined_partition:
                # If fits to any existing equivalence class
                if branch_set.is_similar(model_branch_set,
                                         self._merge_rules):
                    refined_partition[model_branch_set].append(branch_set)
                    break
                # TODO: assert that belongs to 0 or 1 eq. classes
            else:
                # If does not, start new equivalence set
                refined_partition[branch_set] = [branch_set]

        refined_equivalence_classes = refined_partition.values()
        return [BranchSet.from_sets(class_)
                for class_ in refined_equivalence_classes]
