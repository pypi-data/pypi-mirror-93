import networkx as nx

PLUGIN_VERSION = 0


def method(data, seed):
    """Computes the sigma coefficient of the network.

    Parameters
    ----------
    data
        Network whose sigma coefficient is computed.
    seed
        Seed for the random generator.

    Returns
    -------
    float
        The sigma coefficient of the network.

    See Also
    --------
    https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.smallworld.sigma.html
    """

    ddf, d = data
    G = d['data']

    sigma = nx.sigma(G, seed=seed)

    return {'data': sigma}