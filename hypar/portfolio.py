from hypar import stock
from hypar import data_collection
import pandas as pd
import numpy as np

class Portfolio:
    """A collection of Stocks. Serves the purpose of collectively analyzing how
    a group of Stocks performs together over a duration of time. Analysis and
    group operations can be performed on a Portfolio as opposed to having to
    apply the operation to each Stock separately.

    Attributes:
        *stocks (dict[str, Stock]): Stocks belonging to the Portfolio. The key
            of each Stock is its ticker and the value is the Stock itself.
    """

    def __init__(self, *stocks : dict[str, Stock]):
        """Instantiates a Portfolio that contains a dictionary of Stocks.
        The key is the Stock ticker and the value is the Stock itself."""
        # For each Stock in the list entered, create a dict entry with the
        # key being the ticker and the value being the Stock itself.
        port_stocks = dict()
        for s in stocks:
            port_stocks[s.ticker] = s
        self.stocks = port_stocks

    def add_stock(self, *stocks):
        """Adds Stocks to the Portfolio only if the do not already exist.

        Args:
            *stocks (Stock): A Stock and its associated data
        """
        # Only add the Stocks that are not already in the Portfolio.
        to_add = set(stocks).difference(set(self.stocks.keys()))
        for s in to_add:
            self.stocks[s.ticker] = s

    def remove_stock(self, *stocks):
        """Removes Stocks from the Portfolio only if they already exist.

        Args:
            *stocks (Stock): a Stock and its associated data
        """
        # Only remove the Stocks that exist in the Portfolio.
        existing = set(stocks).intersection(set(self.stocks.keys()))
        for s in existing:
            del self.stocks[s]

    def clear(self):
        """Removes all Stocks from the Portfolio, but keeps the Portfolio."""
        # Clear the Portfolio if it contains Stocks
        if len(self.stocks.keys()) != 0:
            self.stocks.clear()
        else:
            print('Portfolio is already empty')

    def preview(self, anonymize=False):
        """Displays a table that contains each Stock, referred to by
        ticker (or pseudonym), the start and end dates of the data, and the
        number of shares owned of each Stock.

        Returns:
            pandas DataFrame with Stock ticker, number of shares, start and end
            dates
        """
        def assign_label(self, stock):
            """Helper method for preview(). Determine the anonymity state of
            the Stock and assign the appropriate label.

            Returns:
                Stock's pseudonym if its anonymity state is True. Otherwise,
                return its ticker.
            """
            is_anonymous, pseuodynm = stock.anonymous[self]
            return pseuodynm if is_anonymous else stock.ticker
        # If preview is to be anonymous, make sure the Stocks are anonymized.
        if not anonymize:
            anonymize(self)
        # List to store number of shares and start/end dates for all Stocks.
        info = []
        # List to store either tickers or pseudonyms for the table.
        index = []
        # For each Stock, determine assign the appropriate label and collect
        # the information to be assigned in the DataFrame.
        for ticker, stock in self.stocks.items():
            if self in stock.portfolios:
                label = assign_label(stock)
            info.append([label,
                        stock.num_shares[self]
                        stock.start_date[self],
                        stock.end_date[self]])
            index.append(label)
        columns = ['Number of Shares', 'Start', 'End']
        return pd.DataFrame(data=info, columns=columns, index=index)

    def total_shares(self):
        """Calculate the total number of shares owned for all Stocks.

        Returns:
            Total number of Stock shares owned in the Portfolio
        """
        return self.preview().sum(axis=1, level='Number of Shares')

    def anonymize(self):
        """Anonymize all Stocks in the Portfolio by setting the bool anonymous
        attribute to True. The ticker symbol is preserved, but is hidden when
        Stock.anonymous is True.
        """
        def generate_pseuodonym(self):
            """Generate a random interger between 0-1000 using
            numpy.random.permutation(1000)[0]. Prepend this with 'S-' to
            complete the pseudonym.

            Returns:
                Pseudonym of the form 'S-xxx' where xxx is a randomly generated
                integer between 0 and 999.
            """
            return 'S-' + str(np.random.permutation(1000)[0])

        # Create a set of existing pseudonyms for all Stocks.
        pseudos = set()
        for stock in self.stocks.values():
            pseudonym = stock.anonymous[self][1]
            pseudos.add(pseudonym)

        # For each Stock in the Portfolio...
        for stock in self.stocks.values():
            # ...get the pseuodynm for the Stock.
            pseuodynm = stock.anonymous[self][1]
            # Until the pseudonym is unique amongst the existing pseudonyms...
            while pseudonym in pseudos:
                # ...generate another pseuodynm.
                pseudonym = generate_pseuodonym(self)
            # Assign this unique pseudonym to the Stock.
            stock.anonymous[self][1] = pseudonym
            # Assign the Stock's anonymity state to True.
            stock.anonymous[self][0] = True

    def reveal(self):
        """ Reveal the ticker symbols of all Stocks in the Portfolio by setting
        each Stock's anonymity state to False.
        """
        for s in self.stocks.values():
            s.anonymous[self][0] = False
