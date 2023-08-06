# source https://gmarti.gitlab.io/networks/2018/06/03/pmfg-algorithm.html

import networkx as nx

PLUGIN_VERSION = 0


def method(data):
    """Compute unweighted PMFG over the network.

    The Planar Maximally Filtered Graph is the planar graph whose edges
    are selected by a greedy algorithm. That is, the edges with greatest
    weight are added one by one to an empty graph so that the resulting
    graph is still planar.

    Parameters
    ----------
    data
        The network whose PMFG is computed.

    Returns
    -------
    networkx.Graph
        PFMG of the given network. The edges has no weight.
    """

    ddf, d = data
    G = d['data']

    pmfg = compute_pmfg(G)

    return {'data': pmfg}


def compute_pmfg(G):
    pmfg = nx.Graph()
    pmfg.add_nodes_from(G.nodes)
    for source, dest, data in get_sorted_edges(G):
        pmfg.add_edge(source, dest)
        is_planar, _ = nx.check_planarity(pmfg)
        if not is_planar:
            pmfg.remove_edge(source, dest)

        if len(pmfg.edges()) == 3 * (len(pmfg.nodes) - 2):
            # theoretical maximum (Euler's formula) is reached
            break

    return pmfg


def get_sorted_edges(G):
    return sorted(
        G.edges(data=True),
        key=lambda x: x[2]['weight'],
        reverse=True
    )