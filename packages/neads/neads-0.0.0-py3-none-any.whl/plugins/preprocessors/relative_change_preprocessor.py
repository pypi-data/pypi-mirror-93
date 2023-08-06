PLUGIN_VERSION = 0


def method(data):
    """Compute relative change series of the time series.

    Parameters
    ----------
    data
        Time series whose relative change series is computed.

    Returns
    -------
    pandas.DataFrame
        The relative change series of the given series.
    """

    ddf, d = data
    df = d['data']

    relative_changes = (df - df.shift(1)) / df.shift(1)
    relative_changes = relative_changes.iloc[1:]

    return {'data': relative_changes}
