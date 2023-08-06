PLUGIN_VERSION = 0


def method(data):
    """Invert weights of edges.

    Parameters
    ----------
    data
        A network whose weights are inverted.

    Returns
    -------
    networkx.Graph
        A network with the same edges, but inverted weights.
    """

    ddf, d = data
    G = d['data']

    F = G.copy()
    for u, v, d in F.edges(data=True):
        d['weight'] = -d['weight']

    return {'data': F}
