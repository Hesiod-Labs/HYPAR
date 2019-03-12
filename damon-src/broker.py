import pandas_datareader.data as pdr
import numpy as np
import matplotlib.pyplot as plt
# package imports
from exceptions import InvalidSourceError
from tutor import *

# np.var, np.std
# golden cross: when the 50 day moves past the 200 day moving average

# MACD


# broker class to simulate some of the trading functionalities
sources = ['yahoo']  # , 'morningstar', 'google', 'quandl'] could do more but they don't work


# tickers must be list even singularly
def broker_main(tickers, start_date, end_date, visual):
    source = 'yahoo'
    # Date, Open, High, Low, Close, Adj Close, Volume
    datasets = [pdr.DataReader(symbol, source, start_date, end_date) for symbol in tickers]
    for data, symbol in zip(datasets, tickers):
        pd.DataFrame(data)
        data['% Change'] = (data['Adj Close'] - data['Open']) / data['Open'] * 100
        # dataset.describe().to_csv(f'{title}-describe.csv')
        data.to_csv(f'/Users/connormcmurry/Desktop/Hesiod Financial/hLabs/HYPAR/broker/broker-src/{symbol}.csv')

    # concatenate and plot all tickers
    frames = pd.DataFrame
    if len(tickers) is 1:
        frames = datasets[0]
        frames['Adj Close'].plot()
        frames['Rolling 50'] = frames['Adj Close'].rolling(50).mean()
        frames['Rolling 200'] = frames['Adj Close'].rolling(200).mean()
    else:
        for data, symbol in zip(datasets, tickers):
            frames[symbol] = data['Adj Close']
        frames.plot()
        frames['Rolling 50'] = frames['Adj Close'].rolling(50).mean()
        frames['Rolling 200'] = frames['Adj Close'].rolling(200).mean()
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title(str(tickers))
    plt.show()


    # scatter two data sets together
    # plot and return the correlation
    plt.scatter(x, y)
    plt.show()

    # there is also np.linspace()
    plt.hist(x, bins=100)
    plt.show()


def noise():
    returns = pd.DataFrame(np.random.normal(1.0, 0.03, (100, 10)))
    prices = returns.cumprod()
    prices.plot()
    plt.show()


def plot_percent_changes(dataset):
    dataset['Percent Change'].plot()
    plt.xlabel('Time')
    plt.ylabel('Percent')
    plt.show()


if __name__ == '__main__':
    broker_main()