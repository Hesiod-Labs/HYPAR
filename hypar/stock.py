from hypar import portfolio
import datetime
import pandas as pd
import numpy as np


class Stock:

    # TODO Complete Attributes
    """A member unit of a Portfolio that contains numerous data attributes.

    Attributes:
        ticker (str): Symbol that represents the Stock entity.
        portfolios (list[Portfolio]): One or more Portfolios of which the Stock
            is a member. The list contains all portfolios to which the stock
            belongs.
        num_shares (dict[Portfolio, int]): Number of shares owned in each
            Portfolio. Each key is a Portfolio and the value is number of
            shares.
        start_date (dict[Portfolio, datetime]): Earliest data entry of the Stock
            in each Portfolio. Each key is a Portfolio and each value is the
            start date.
        end_date (dict[Portfolio, datetime]): Most recent data entry of the
            Stock in each Portfolio. Each key is a Portfolio and each value is
            the end date.
        price_data (dict):
        balance_sheet (dict):
        book_data (dict):
        cash_flow (dict):
        company_data (dict):
        earnings (dict):
        income_statement (dict):
        intraday_data (dict):
        key_stats (dict):
        price_target (dict):
        anonymous (dict[Portfolio, dict[bool, str]): Each key is Portfolio and
            each value is a list pair: if index 0 is True, the Stock is
            "anonymous" and the pseudonym in index 1 string is displayed;
            otherwise, the real ticker is displayed. Pseudonym format is 'S-xxx'
            where 'xxx' is a randomly generated intger between 0-999.
    """

    def __init__(self, ticker, portfolios=None, num_shares=[1],
                start_date=None, end_date=None, price_data=None,
                balance_sheet=None, book_data=None, cash_flow=None,
                company_data=None, earnings=None, income_statement=None,
                intraday_data=None, key_stats=None, price_target=None,
                anonymous=None):
        """Instantiates a Stock with any associated data."""
        self.ticker = str.upper(ticker)
        # TODO Make this a set?
        self.portfolios = portfolios
        self.num_shares = num_shares
        self.start_date = start_date
        self.end_date = end_date
        self.price_data = price_data
        self.balance_sheet = balance_sheet
        self.book_data = book_data
        self.cash_flow = cash_flow
        self.company_data = company_data
        self.earnings = earnings
        self.income_statement = income_statement
        self.intraday_data = intraday_data
        self.key_stats = key_stats
        self.price_target = price_target
        self.anonymous = anonymous
