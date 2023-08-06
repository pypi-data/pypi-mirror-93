from networkx.algorithms.community import girvan_newman

PLUGIN_VERSION = 0


def method(data, communities_count):
    """Compute node clustering by Girvan-Newman algorithm.

    Parameters
    ----------
    data
        A network whose clusters are computed.
    communities_count
        Number of communities to be found.

    Returns
    -------
    tuple(tuple(Node))
        Returns a sequence of clusters. Each cluster is
        represented as a tuple of nodes which belongs to the cluster.
    """

    ddf, d = data
    G = d['data']
    com = girvan_newman(G)
    result = _extract_clustering_by_community_count(com, communities_count)
    return {'data': result}


def _extract_clustering_by_community_count(gn_generator, count):
    # clustering on index 0 in generator has two clusters
    # ie. clustering on index i-2 has i clusters
    from itertools import islice
    return next(islice(gn_generator, count-2, None))
