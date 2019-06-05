import pandas as pd
import numpy as np
import quandl 
import pyEX.stocks as pyex
import os
import csv
from hypar_package import Stock
from hypar_package import Portfolio


def generate_portfolio():
    """ Main method for creating a Portfolio that contains Stock and Stock data.

    Returns:
        The Portfolio containing user requested stocks and data.
    """
    def check_for_api_tokens():
        """Assigns the API token and version to use when calling the API.

        The user specifies the version of the IEX Cloud API to call.
            - "stable" calls real API data; counts towards monthly API allowance
            - "sandbox" calls fake API data; does not count towards monthly API allowance
        
        If the user has previously used that version before, the API token will be retrieved,
        and does not require re-entering by the user.
        
        Returns:
            API version corresponding token to collect data.
        """

        # Name of the csv .txt file that contains user-specific API tokens
        tokens = 'iex_api_tokens.txt'
    
        # Ask for which version of the API to call
        api_env = input('Enter "stable" for real data and "sandbox" for test data: ')

        # Check if iex_api_tokens.txt exists
        if os.path.exists(tokens):
        
            # Check to see if this version token exists in the .txt file
            with open(tokens, 'r') as csv_file:
                reader = csv.DictReader(csv_file, delimiter=',')
                version_exists = [False, None]
                
                for row in reader:

                    # If it does, set the api key to be used to call the data
                    if row['version'] == api_env:
                        version_exists[0] = True
                        version_exists[1] = row['token'] 

                if version_exists[0]:
                    api_key = version_exists[1]

                # If the version has not been used before, ask the user for the version token
                # and at the information to the .txt file
                else:
                    api_key = input('Enter your IEX Cloud API key: ')
                    with open(tokens, 'a') as csv_file:
                        fields = ['version', 'token']
                        writer = csv.DictWriter(csv_file, fieldnames=fields)
                        writer.writerow({'version': api_env, 'token': api_key})
        
        # .txt file does not exist
        else:
            api_key = input('Enter your IEX Cloud API key: ')

            # Add the version/token entry to the .txt file
            with open(tokens, 'a') as csv_file:
                fields = ['version', 'token']
                writer = csv.DictWriter(csv_file, fieldnames=fields)
                writer.writeheader()
                writer.writerow({'version': api_env, 'token': api_key})

        return api_env, api_key
    
    def define_iex_call():

        """ Set the timeframe and data to be collected from the API.

        The pre-determined timefrimes align with those defined in the API.
        Enter the number corresponding to the kind of data to call from the API.
        Each number corresponds to a function defined by the pyEX library and 
        a unit cost (if using any other version of IEX besides "sandbox").

        The input string of numbers are then split and subsequently used to call 
        the method contained in pyEX, obtain the data from IEX, and assign it to the 
        appropriate attribute of the Stock.

        Returns:
            IEX API call specifications (i.e., data types and timeframe)
        """

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
        
        return timeframe, data_dict, data

    def generate_stock(ticker, position_in_list):
        
        """ Main method for creating Stocks based on user specified information.

        A Stock is first generated by setting its ticker, which is based on user input.
        From the specified information to be collected from IEX, a Stock's other attributes
        are subsequently assigned with the appropriate information in accordance with the
        IEX version, token, and timeframe.

        Returns:
            A Stock object containing information on the stock.
        """

        stock = Stock.Stock(ticker)

        for i in requested_data:
            if i == 1:
                setattr(stock, ref_data[i][0], 
                        ref_data[i][1](tickers[position_in_list],
                                        timeframe=timeframe,
                                        token=api_key, 
                                        version=api_env))
            else:
                setattr(stock, ref_data[i][0], 
                    ref_data[i][1](tickers[position_in_list], 
                                    token=api_key, 
                                    version=api_env))
        return stock

    # Specify IEX information 
    api_env, api_key = check_for_api_tokens()

    # Specify tickers to search
    tickers = input('Symbols (separate with comma): ')
    tickers = tickers.split(',')
    
    for i, t in enumerate(tickers):
        tickers[i] = t.strip()

    # Create an empty Portfolio to store the stocks
    portfolio = Portfolio.Portfolio()

    # Specify the IEX data and timeframe
    timeframe, ref_data, requested_data = define_iex_call()

    # For each ticker listed by the user, create a Stock object
    # and add it to the Portfolio
    for i, t in enumerate(tickers):
        stock  = generate_stock(t, i)
        portfolio.add_stock(stock)

    return portfolio