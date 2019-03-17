import pandas_datareader.data as pdr
# package imports
from tutor import *
from exceptions import SourceException


sources = ['yahoo']  # 'morningstar', 'google', 'quandl'], could do more but they don't work


# tickers must be list even singularly
def broker(tickers, source, start_date, end_date):
    if source not in sources:
        raise SourceException('the source provided is either invalid or not accepted')
    # Date, High, Low, Open, Close, Adj Close, Volume
    datasets = [pdr.DataReader(symbol, source, start_date, end_date) for symbol in tickers]
    for data, symbol in zip(datasets, tickers):
        pd.DataFrame(data)
        data['% Change'] = (data['Close'] - data['Open']) / data['Open'] * 100
        data['R50'] = data.rolling(50).mean()
        data['R200'] = data.rolling(200).mean()
        # dataset.describe().to_csv(f'{symbol}-describe.csv') <- append to front/back of CSV
        # data.to_csv(wherever we should store the files)
    if len(datasets) is 1:
        return datasets[0]
    return datasets
