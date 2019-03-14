# testing class for the paladin method
from broker import broker
from correlation import *


def test_broker():
    broker('AMZN', 'yahoo' '2015-01-01', '2018-01-01')
    broker(['INTC', 'NVDA', 'XLNX'], 'yahoo' '2015-01-01', '2018-01-01')


def test_correlation_main():
    intel = broker('INTC', 'yahoo' '2015-01-01', '2018-01-01')
    nvidia = broker('NVDA', 'yahoo' '2015-01-01', '2018-01-01')
    print(correlation(intel, 'INTC', nvidia, 'NVDA'))
    correlation(intel, 'INTC', nvidia, 'NVDA', 'linear')
    correlation(intel, 'INTC', nvidia, 'NVDA', 'scatter')

