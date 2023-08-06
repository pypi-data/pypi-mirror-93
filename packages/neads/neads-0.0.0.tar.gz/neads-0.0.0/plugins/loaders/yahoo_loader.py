import pandas_datareader.data as web

PLUGIN_VERSION = 0


def method(data, company_list, start, end):
    """Yahoo loader for downloading financial data.

    Parameters
    ----------
    data
        Method does not use this parameter. It is there only for formal
        purposes.
    company_list : tuple(string)
        A sequence of tickers of companies whose data are loaded.
    start
        Start date of the data.
    end
        End data of the data.

    Returns
    -------
    pandas.Dataframe
        A DataFrame with the company time series of the columns.
    """

    # Download the data
    raw_df = web.DataReader(
        company_list,
        start=start,
        end=end,
        data_source='yahoo'
    )['Adj Close']

    # Deleting companies with empty record
    df = raw_df.loc[:, raw_df.notna().all()]

    return {'data': df}
