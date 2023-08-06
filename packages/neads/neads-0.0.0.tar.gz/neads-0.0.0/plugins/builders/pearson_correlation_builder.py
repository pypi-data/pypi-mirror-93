import networkx as nx

PLUGIN_VERSION = 0


def method(data):
    """Compute a weighted networks using the Pearson correlation.

    The Pearson correlation of pairs of series defines the weights in
    the network.

    Parameters
    ----------
    data : pandas.DataFrame
        Time series to be transformed into network.

    Returns
    -------
    networkx.Graph
        Weighted network whose weights are determined by Pearson
        correlation of the series of the adjacent nodes.
    """

    ddf, d = data
    df = d['data']

    G = nx.from_pandas_adjacency(df.corr())
    G.remove_edges_from(nx.selfloop_edges(G))

    return {'data': G}
