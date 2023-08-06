PLUGIN_VERSION = 0


def method(data):
    """Counts number of edges in the network.

    Parameters
    ----------
    data
        Network whose edges are counted.

    Returns
    -------
    int
        Number of edges of the network.
    """

    ddf, d = data
    G = d['data']

    edge_count = len(G.edges)

    return {'data': edge_count}