# testing class for the paladin method
from broker import broker
from correlation import *
from blackscholes import blackscholes


def test_broker():
    broker('AMZN', 'yahoo' '2015-01-01', '2018-01-01')
    broker(['INTC', 'NVDA', 'XLNX'], 'yahoo' '2015-01-01', '2018-01-01')


def test_correlation_main():
    amazon = broker('AMZN', 'yahoo', '2015-01-01', '2018-01-01')
    nvidia = broker('NVDA', 'yahoo', '2015-01-01', '2018-01-01')
    print(correlation(amazon, 'AMZN', nvidia, 'NVDA'))
    correlation(amazon, 'AMZN', nvidia, 'NVDA', 'linear')
    correlation(amazon, 'AMZN', nvidia, 'NVDA', 'scatter')


def test_black_scholes():
# example parameters: stock_price = 100, strike_price = 100, expiration = 1 aka 1 year, rfr = 0.05, sigma = 2
    print(blackscholes(100, 100, 1, 0.05, 2, 'call'))

