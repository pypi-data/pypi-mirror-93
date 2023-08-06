PLUGIN_VERSION = 0


def method(data):
    """Normalize weights of edges.

    Weight of each edges is divided by the greatest weight of the absolute
    values of the edges. That is, the greater absolute value of all weights
    will be 1.

    Parameters
    ----------
    data
        A network whose weights are normalized.

    Returns
    -------
    networkx.Graph
        A network with the same edges, but inverted weights.
    """

    ddf, d = data
    G = d['data']

    F = G.copy()
    max_weight = max(abs(d['weight']) for u, v, d in F.edges(data=True))
    for u, v, d in F.edges(data=True):
        d['weight'] = d['weight'] / max_weight

    return {'data': F}
