import networkx as nx

PLUGIN_VERSION = 0


def method(data, quotient):
    """Preserve only the given quotient of edges in the given network.

    Only the edges with greatest weight stay in the graph.

    Parameters
    ----------
    data
        The network whose edges are filtered.
    quotient
        The ratio of edges to stay.

    Returns
    -------
    networkx.Graph
        Unweighted network with only a given quotient of edges.
    """

    ddf, d = data
    G = d['data']

    sorted_edges = sorted(
        G.edges(data=True),
        key=lambda e: e[2]['weight'],
        reverse=True
    )
    significant_edges = sorted_edges[:int(quotient*len(sorted_edges))]
    F = nx.Graph()
    F.add_nodes_from(G.nodes())
    F.add_edges_from((u, v) for u, v, d in significant_edges)

    return {'data': F}