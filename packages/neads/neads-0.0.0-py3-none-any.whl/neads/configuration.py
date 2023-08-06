"""Module providing Configuration class."""

# TODO: move here construction of NeadsGraph.

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neads.phases import Loading, Preprocessing, Evolution, Building, \
        WeightedEditing, Filtering, UnweightedEditing, Analyzing, \
        Finalizing


class Configuration:
    """Description of a process whose execution leads to a particular data.

    More precisely, configuration describes a tree of intermediate
    results. That is a graph whose nodes are the intermediate (and
    also the final) results of the computation.

    Each of these result is produced by a particular plugin with particular
    parameters. Oriented edges of the graph captures data dependency
    between its nodes, ie. what was the inputting data of the plugin that
    produced the result of the node.

    The configuration itself consist of phases, each of which has its
    own purpose in the computation process. See their documentation for
    more details.
    """

    def __init__(self,
                 loading: Loading,
                 preprocessing: Preprocessing,
                 evolution: Evolution,
                 building: Building,
                 weighted_editing: WeightedEditing,
                 filtering: Filtering,
                 unweighted_editing: UnweightedEditing,
                 analyzing: Analyzing,
                 finalizing: Finalizing):
        """Initialize Configuration.

        All phases must be passed as argument. However, many of them
        might be empty (ie. they needn't contain any PluginRecord).

        Loading must always be non-empty, even as an empty method.
        Finalizing must be present because by definition, they describe
        the final results.

        Presence of plugins in the other phases is up to user. However,
        it is their responsibility that API of the successive Plugins
        if compatible.

        Parameters
        ----------
        loading
            Non-empty loading layer for loading initial time series.
        preprocessing
            Preprocessing layer for altering the data.
        evolution
            Evolution layer for splitting the time series into
            (typically overlapping) intervals.
        building
            Building layer for creating a network (usually weighted)
            from given time series.
        weighted_editing
            Weighted editing layer for altering the weighted network.
        filtering
            Filtering layer for *filtering out* the weights,
            ie. producing unweighted network.
        unweighted_editing
            Unweighted editing layer for altering the unweighted network.
        analyzing
            Analyzing layer for computing a network characteristics.
        finalizing
            Finalizing layer for gathering data produced in the process
            and outputting the final results.
        """

        self.loading = loading
        self.preprocessing = preprocessing
        self.evolution = evolution
        self.building = building
        self.weighted_editing = weighted_editing
        self.filtering = filtering
        self.unweighted_editing = unweighted_editing
        self.analyzing = analyzing
        self.finalizing = finalizing

    @property
    def is_evolving(self) -> bool:
        """Return, whether the evolution phase is non-empty."""
        return not self.evolution.empty
