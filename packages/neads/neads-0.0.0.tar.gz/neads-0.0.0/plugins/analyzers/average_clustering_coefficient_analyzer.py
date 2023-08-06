import networkx as nx

PLUGIN_VERSION = 0


def method(data):
    """Computes the average clustering coefficient of the network.

    Parameters
    ----------
    data
        Network whose average clustering coefficient is computed.

    Returns
    -------
    float
        The average clustering coefficient of the network.
    """

    ddf, d = data
    G = d['data']

    average_clustering_coef = nx.average_clustering(G)

    return {'data': average_clustering_coef}