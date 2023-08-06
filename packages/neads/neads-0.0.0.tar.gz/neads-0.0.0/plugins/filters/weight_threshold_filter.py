import networkx as nx

PLUGIN_VERSION = 0


def method(data, threshold):
    """Preserve only the edges whose weight is at least the threshold.

    Parameters
    ----------
    data
        The network whose edges are filtered.
    threshold
        The minimum weight of edge to stay in the network.

    Returns
    -------
    networkx.Graph
        Unweighted network with edges whose weight was at least the
        threshold.
    """

    ddf, d = data
    G = d['data']

    significant_edges = [(u, v) for u, v, e in G.edges(data=True)
                         if e['weight'] >= threshold]
    F = nx.Graph()
    F.add_nodes_from(G.nodes())
    F.add_edges_from(significant_edges)

    return {'data': F}
