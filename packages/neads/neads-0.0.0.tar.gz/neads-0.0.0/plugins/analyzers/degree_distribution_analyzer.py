from collections import Counter

PLUGIN_VERSION = 0


def method(data):
    """Computes the degree distribution of the network.

    Parameters
    ----------
    data
        Network whose degree distribution is computed.

    Returns
    -------
    degrees : tuple(int)
        Sequence of degrees.
    count: tuple(int)
        Sequence of number of nodes of the degree on the corresponding
        index `degrees`.
    """

    ddf, d = data
    G = d['data']

    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    degree_count = Counter(degree_sequence)
    deg, cnt = zip(*degree_count.items())

    return {'data': (deg, cnt)}
