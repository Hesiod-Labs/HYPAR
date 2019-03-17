# testing class for the paladin method
from broker import broker
from correlation import *


def test_broker():
    broker('AMZN', 'yahoo' '2015-01-01', '2018-01-01')
    broker(['INTC', 'NVDA', 'XLNX'], 'yahoo' '2015-01-01', '2018-01-01')


def test_correlation_main():
    amazon = broker('AMZN', 'yahoo', '2015-01-01', '2018-01-01')
    nvidia = broker('NVDA', 'yahoo', '2015-01-01', '2018-01-01')
    print(correlation(amazon, 'AMZN', nvidia, 'NVDA'))
    correlation(amazon, 'AMZN', nvidia, 'NVDA', 'linear')
    correlation(amazon, 'AMZN', nvidia, 'NVDA', 'scatter')

