from statistics import mean

PLUGIN_VERSION = 0


def method(data):
    """Computes the average degree of the network.

    Parameters
    ----------
    data
        Network whose average degree is computed.

    Returns
    -------
    float
        The average degree of the network.
    """

    ddf, d = data
    G = d['data']

    degrees = dict(G.degree()).values()
    average_degree = mean(degrees)

    return {'data': average_degree}