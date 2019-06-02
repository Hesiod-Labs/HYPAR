import datetime
import pandas as pd


class Stock:

    def __init__(self, ticker, owned=True, num_shares=1, start_date=None,
                 end_date=None, price_data=None, balance_sheet=None,
                 book_data=None, cash_flow=None, company_data=None,
                 earnings=None, income_statement=None,
                 intraday_data=None, key_stats=None, price_target=None,
                 anonymous=False):

        self.ticker = str.upper(ticker)
        self.owned = owned
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