import networkx as nx

PLUGIN_VERSION = 0


def method(data):
    """Extract largest connected component of the given network.

    Parameters
    ----------
    data
        A network whose largest component is extracted.

    Returns
    -------
    networkx.Graph
        A network of the largest component.
    """

    ddf, d = data
    G = d['data']

    component = max(nx.connected_components(G), key=len)
    component_graph = G.subgraph(component).copy()

    return {'data': component_graph}