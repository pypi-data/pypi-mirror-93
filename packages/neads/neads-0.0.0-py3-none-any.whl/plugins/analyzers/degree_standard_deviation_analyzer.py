from statistics import stdev

PLUGIN_VERSION = 0


def method(data):
    """Computes the standard deviation of degrees of the network.

    Parameters
    ----------
    data
        Network whose standard deviation of degrees is computed.

    Returns
    -------
    float
        The standard deviation of degrees of the network.
    """

    ddf, d = data
    G = d['data']

    degrees = dict(G.degree()).values()
    degree_stdev = stdev(degrees)

    return {'data': degree_stdev}