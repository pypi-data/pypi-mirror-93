import networkx as nx
from statistics import mean
from itertools import chain

PLUGIN_VERSION = 0


def method(data):
    """Computes the average path length of the network.

    Parameters
    ----------
    data
        Network whose average path length is computed.

    Returns
    -------
    float
        The average path length of the network.
    """

    ddf, d = data
    G = d['data']

    apl = _average_shortest_path(G)

    return {'data': apl}


def _average_shortest_path(G):
    # between only reachable pairs
    source_target_dict = dict(nx.all_pairs_shortest_path_length(G))
    lists_of_lengths = [d.values() for d in source_target_dict.values()]
    flat_lengths = chain.from_iterable(lists_of_lengths)
    # for each s-t pair is their distance counted twice
    # but it does not corrupt the mean
    return mean(flat_lengths)