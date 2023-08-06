PLUGIN_VERSION = 0


def method(data, length, shift):
    """Compute evolution intervals using fix window length and shift.

    All the resulting intervals have the same length. They start with
    the interval [0, length). Some data points at the end of the series
    may be cropped, if they fit in no interval.

    Parameters
    ----------
    data
        The time series on which the evolution intervals are computed.
    length
        Length of the sliding windows. Number of data points in an
        interval will be determined by the length.
    shift
        Shift of the sliding window, again in number of data points. The
        i-th interval is [i*shift, length + i*shift).

    Returns
    -------
    tuple((start, end))
        A sequence of intervals. Each interval is described by starting
        index and ending index, i.e. [start, end).
    """

    ddf, d = data
    df = d['data']

    index_limit = len(df.index)
    intervals = []
    start = 0
    while start + length <= index_limit:
        intervals.append((start, start + length))
        start += shift

    return {'data': intervals}
