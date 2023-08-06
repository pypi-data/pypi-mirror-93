"""Module providing classes defining particular data produced by plugins.

Data arise as by a sequence of modifications of an initial data (produced
by loader). Each of these modification, ie. change by one plugin,
is captured by DataDefinitionComponent. A whole sequence of modifications
is captured by DataDefinition instances.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Set, Tuple

if TYPE_CHECKING:
    from neads.nodes import Node
    from neads.plugin_use import PluginUse


class DataDefinitionComponent:
    """Class describing one use of a particular plugin.

    Attributes
    ----------
    name : str
        Name of used plugin.
    version : int
        Version of used plugin.
    params : dict
        Params with which the plugin was used.
    """

    def __init__(self, plugin_use: PluginUse):
        """Initialize instance by providing all corresponding PluginUse.

        The DataDefinitionComponent basically describes a particular
        PluginUse. The DDC just copies all the information from the
        given instance.

        Parameters
        ----------
        plugin_use : PluginUse
            PluginUse which will be captured in the initialized instance.
        """

        self.name = plugin_use.name
        self.version = plugin_use.version
        self.params = plugin_use.params

    def __eq__(self, other: DataDefinitionComponent) -> bool:
        """Return whether self is equal to the other DDC.

        The equality check is done by comparing corresponding
        attributes, ie. self.name with other.name and so on. True is
        returned iff all the pairs match.

        Parameters
        ----------
        other : DataDefinitionComponent
            The other definition component to be compared with self.

        Returns
        -------
        bool
            True, if all the corresponding attributes are equal.
            Otherwise False.
        """

        return self.name == other.name \
            and self.params == other.params \
            and self.version == other.version

    def to_hashable(self):
        # TODO: kill this method
        #  it should have been correctly hashable directly!!
        #  define method __hash__
        return (
            self.name,
            self.version,
            tuple(sorted(self.params.items(), key=lambda pair: pair[0]))
        )


class DataDefinition:
    """Class describing a sequence of modification characterising the data.

    Attributes
    ----------
    components : Tuple[DataDefinitionComponent]

    """

    def __init__(self, node: Node):
        """Initialize instance by providing node that produced the data.

        The DataDefinition describes gradual modifications from which
        arose the final data. The given node is the last in the series
        of modifications, the rest is determined by its predecessors.

        Parameters
        ----------
        node : Node
            The last node that modified the data.
        """

        # TODO: delete node, it is completely excessive
        self.node = node
        self.components = self._get_components(node)

    def _get_components(self, node) -> Tuple[DataDefinitionComponent]:
        """Return the sequence of modifications.

        Each step of modification is described by corresponding
        DataDefinitionComponent.

        Parameters
        ----------
        node
            The last node of the sequence of modifications.

        Returns
        -------
        Tuple[DataDefinitionComponent]
            Sequence of modifications described by corresponding
            DataDefinitionComponents.
        """

        # Exploiting the fact that for all important nodes, ie. not
        # finalizers, each preceding node has different level
        nodes_to_top = self._get_nodes_to_top(node)
        # Completely stupid solution, as some nodes may have an equal depth
        return tuple(n.get_data_definition_component()
                     for n
                     in sorted(nodes_to_top, key=lambda n: n.get_depth()))

    def _get_nodes_to_top(self, base_node) -> Set[Node]:
        """Returns ancestors of the given node."""
        def visit(node):
            if node not in visited:
                visited.add(node)
                for parent in node.parents:
                    visit(parent)

        visited = set()
        visit(base_node)
        return visited

    def __eq__(self, other: DataDefinition) -> bool:
        """Returns whether the is an equality."""
        return all([self_comp == other_comp
                    for self_comp, other_comp
                    in zip(self.components, other.components)])

    def to_hashable(self):
        # TODO: kill this method
        #  it should have been correctly hashable directly!!
        #  define method __hash__
        return tuple(comp.to_hashable() for comp in self.components)
