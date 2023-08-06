from networkx.algorithms.community import asyn_fluidc

PLUGIN_VERSION = 0


def method(data, communities_count, max_iter, seed):
    """Compute node clustering by FluidC algorithm.

    Parameters
    ----------
    data
        A network whose clusters are computed.
    communities_count
        Number of communities to be found.
    max_iter
        Number of iteration of the algorithm.
    seed
        Seed of the algorithm (as the initialization is random).

    Returns
    -------
    tuple(tuple(Node))
        Returns a sequence of clusters. Each cluster is
        represented as a tuple of nodes which belongs to the cluster.
    """

    ddf, d = data
    G = d['data']
    gen = asyn_fluidc(G, communities_count, max_iter=max_iter, seed=seed)
    return {'data': tuple(gen)}
