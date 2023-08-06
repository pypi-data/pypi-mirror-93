import matplotlib.pyplot as plt

PLUGIN_VERSION = 0


def method(data):
    """Plot a log-log plot of the given data.

    Parameters
    ----------
    data
        Two sequences of data, one for the x-axis and the other for the
        y-axis.
    """

    ddf, d = data
    x, y = d['data']
    plt.loglog(x, y)
