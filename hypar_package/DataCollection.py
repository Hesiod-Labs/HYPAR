import pandas as pd
import numpy as np
import quandl 
import pyEX.stocks as pyex

from hypar_package import Stock
from hypar_package import Portfolio

def generate_portfolio():
    
    api_env = input('Enter "stable" for real data and "sandbox" for test data: ')
    api_key = input('Enter your IEX Cloud API key: ')
    tickers = input('Symbols (separate with comma): ')
    tickers = tickers.split(',')
    
    for i, t in enumerate(tickers):
        tickers[i] = t.strip()
    
    timeframe = input('Timeframe (max (15yr), 5y, 2y, 1y, ytd, 6m, 3m, 1m): ')
    
    data_dict = {1: ('price_data', pyex.chartDF, 10),
                2: ('balance_sheet', pyex.balanceSheetDF, 3000),
                3: ('book_data', pyex.bookDF, 1),
                4: ('cash_flow', pyex.cashFlowDF, 1000),
                5: ('company_data', pyex.companyDF, 1),
                6: ('earnings', pyex.earningsDF, 1000),
                7: ('income_statement', pyex.incomeStatementDF, 1000),
                8: ('intraday_data', pyex.intradayDF, 1),
                9: ('key_stats', pyex.keyStatsDF, 5),
                10: ('price_target', pyex.priceTarget, 500)}
    
    print('Type the numbers corresponding to the data of interest (separate with comma): ')
    print('[1] price data')
    print('[2] balance sheet')
    print('[3] book data')
    print('[4] cash flow')
    print('[5] company data')
    print('[6] earnings')
    print('[7] income statement')
    print('[8] intraday data')
    print('[9] key stats')
    print('[10] price target')
    
    data = input()
    data = data.split(',')
    
    for i, n in enumerate(data):
        data[i] = int(n)
    
    portfolio = Portfolio.Portfolio()
    
    def generate_stock(ticker):
        
        stock = Stock.Stock(ticker)

        for i in data:
            if i is 1:
                setattr(stock, data_dict[i][0], 
                        data_dict[i][1](tickers[i-1],
                                        timeframe=timeframe,
                                        token=api_key, 
                                        version=api_env))
            setattr(stock, data_dict[i][0], 
                data_dict[i][1](tickers[i-1], 
                                token=api_key, 
                                version=api_env))
        return stock
                
    for t in tickers:
        stock  = generate_stock(t)
        portfolio.add_stock(stock)
        
    return portfolio
