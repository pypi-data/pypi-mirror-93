PLUGIN_VERSION = 0


def method(data):
    """Preserve all edges, only removes their weight.

    Parameters
    ----------
    data
        The network whose edges are filtered.

    Returns
    -------
    networkx.Graph
        Unweighted network with the same edges as the given network.
    """

    ddf, d = data
    G = d['data']

    F = G.copy()
    for u, v, d in F.edges(data=True):
        del d['weight']

    return {'data': F}
