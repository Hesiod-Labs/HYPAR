from hypar_package import Stock
from hypar_package import DataCollection

class Portfolio:
    """
    A collection of Stocks.

    """

    def __init__(self, *stocks):
        """
           Contains all acquired assets.

           Args:
               stocks (Stock): list of stocks belonging to the portfolio.

        """

        self.stocks = list(stocks)
        
    def add_stock(self, stock):
      self.stocks.append(stock)

    def remove_stock(self, stock):
      self.stocks.remove(stock)

    def clear(self):
      self.stocks.clear()

    def preview(self):
      for i, s in enumerate(self.stocks):
        if s.anonymous:
          print('S' + str(i), s.num_shares)
        else:
          print(s.ticker, s.num_shares)

    def list_tickers(self):
      tickers = []
      for s in self.stocks:
        tickers.append(s.ticker)
      return tickers

    def get_stock(self, ticker):
      return self.stocks[self.list_tickers().index(ticker)]
      
    def anonymize(self):
      for s in self.stocks:
        s.anonymous = True

    def reveal(self):
      for s in self.stocks:
        s.anonymous = False