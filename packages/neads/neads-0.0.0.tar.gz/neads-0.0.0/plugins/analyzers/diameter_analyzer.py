import networkx as nx
import numpy as np

PLUGIN_VERSION = 0


def method(data):
    """Computes the diameter of the network.

    Parameters
    ----------
    data
        Network whose diameter is computed.

    Returns
    -------
    float
        The diameter of the network.
    """

    ddf, d = data
    G = d['data']

    if nx.is_connected(G):
        diam = nx.diameter(G)
    else:
        diam = np.infty

    return {'data': diam}