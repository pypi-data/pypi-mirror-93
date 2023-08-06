PLUGIN_VERSION = 0


def method(data, window_length):
    """Compute moving average series of the time series.

    Parameters
    ----------
    data
        Time series whose moving average series is computed.
    window_length
        Length of the window over which the average is computed.

    Returns
    -------
    pandas.DataFrame
        The moving average series of the given series.
    """

    ddf, d = data
    df = d['data']

    moving_average = df.rolling(window_length).mean()
    moving_average = moving_average.iloc[window_length - 1:]

    return {'data': moving_average}