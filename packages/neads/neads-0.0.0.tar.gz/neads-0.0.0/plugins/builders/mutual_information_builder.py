from pyinform.mutualinfo import mutual_info
import networkx as nx

PLUGIN_VERSION = 0

c = 1000


def method(data, normalize):
    """Compute a weighted networks using the mutual information.

    The mutual information between pairs of series defines the weights in
    the network.

    Parameters
    ----------
    data : pandas.DataFrame
        Time series to be transformed into network.
    normalize : bool
        Whether the weights are normalized, so that the greatest value
        is 1.

    Returns
    -------
    networkx.Graph
        Weighted network whose weights are determined by mutual
        information of the series of the adjacent nodes.
    """

    ddf, d = data
    df = d['data']

    mutual_info_matrix = df.corr(method=mutual_info_wrapper)
    if normalize:
        max_entry = mutual_info_matrix.max().max()
        mutual_info_matrix = mutual_info_matrix / max_entry
    G = nx.from_pandas_adjacency(mutual_info_matrix)
    G.remove_edges_from(nx.selfloop_edges(G))

    return {'data': G}


def mutual_info_wrapper(series_a, series_b):
    scaled_a = c*series_a + c
    scaled_b = c*series_b + c
    return mutual_info(scaled_a, scaled_b)
