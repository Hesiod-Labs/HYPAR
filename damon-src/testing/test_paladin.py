# testing class for the paladin method
import numpy as np
from broker import *
from normallity import *
from correlation import *



def test_data_retrieval():
    # add volume
    show_data(dataset)


def test_charts():
    scatter(dataset['Adj Close'], dataset['Volume'])
    histogram(dataset['Adj Close'])
    noise()


def test_write_report():
    write_report(dataset, '/Users/connormcmurry/Desktop/Hesiod Financial/hLabs/HYPAR/broker/broker-src/Test')


def test_percent_change():
    map_percent_return(dataset)
    write_report(dataset, '/Users/connormcmurry/Desktop/Hesiod Financial/hLabs/HYPAR/broker/broker-src/pct-chng')


def test_plotting_percents():
    map_percent_return(dataset)
    plot_percent_changes(dataset)


def test_formatted_data():
    map_percent_return(dataset)
    print(format_data(dataset, 1.5))


def test_jarque_bera():
    map_percent_return(dataset)
    jbt = jarque_bera_test(dataset['Percent Change'])
    print(jbt)


def test_rolling_correlations():
    map_percent_return(dataset)
    map_percent_return(dataset_two)
    rolling_correlation(dataset['Percent Change'], dataset_two['Percent Change'], 60)


def test_correlation_main():
    correlation_main('INTC', 'NVDA', '2015-01-01', '2018-01-01', 'linear')


def test_broker():
    tickers = ['INTC', 'NVDA', 'XLNX']
    broker_main(tickers, '2015-01-01', '2018-01-01')
