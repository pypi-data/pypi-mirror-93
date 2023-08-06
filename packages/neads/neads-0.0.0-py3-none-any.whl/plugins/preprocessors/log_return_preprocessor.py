import numpy as np

PLUGIN_VERSION = 0


def method(data):
    """Compute logarithmic return series of the time series.

    Parameters
    ----------
    data
        Time series whose logarithmic return series is computed.

    Returns
    -------
    pandas.DataFrame
        The logarithmic return series of the given series.
    """

    ddf, d = data
    df = d['data']
    log_ret = np.log(df) - np.log(df.shift(1))
    return {'data': log_ret.iloc[1:]}  # without first row with NaNs
