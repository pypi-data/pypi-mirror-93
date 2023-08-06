PLUGIN_VERSION = 0


def method(data):
    """Counts number of nodes in the network.

    Parameters
    ----------
    data
        Network whose nodes are counted.

    Returns
    -------
    int
        Number of nodes of the network.
    """

    ddf, d = data
    G = d['data']

    node_count = len(G.nodes)

    return {'data': node_count}