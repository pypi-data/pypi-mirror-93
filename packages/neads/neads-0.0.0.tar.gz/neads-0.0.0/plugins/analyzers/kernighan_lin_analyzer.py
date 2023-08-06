from networkx.algorithms.community import kernighan_lin_bisection


PLUGIN_VERSION = 0


def method(data, max_iter, seed):
    """Compute node set bisection by Kernighan-Lin algorithm.

    Parameters
    ----------
    data
        A network whose node are split into two sets.
    max_iter
        Number of iteration of the algorithm.
    seed
        Seed of the algorithm (as the initialization is random).

    Returns
    -------
    tuple(tuple(Node), tuple(Node))
        Returns two tuple of the nodes as they are divided into two sets
        by the algorithm.
    """

    ddf, d = data
    G = d['data']
    result = kernighan_lin_bisection(G, max_iter=max_iter, seed=seed)
    return {'data': result}
