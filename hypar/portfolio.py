from hypar.stock import Stock as stock
import pandas as pd
import numpy as np
from collections import OrderedDict


class Portfolio:
    """A collection of Stocks. Serves the purpose of collectively analyzing how
    a group of Stocks performs together over a duration of time. Analysis and
    group operations can be performed on a Portfolio as opposed to having to
    apply the operation to each Stock separately.

    Attributes:
        *stocks (dict[str, Stock]): Stocks belonging to the Portfolio. The key
            of each Stock is its ticker and the value is the Stock itself.
    """

    def __init__(self, *stocks: stock):
        """Instantiates a Portfolio that contains a dictionary of Stocks.
        The key is the Stock ticker and the value is the Stock itself."""
        # For each Stock in the list entered, create a dict entry with the
        # key being the ticker and the value being the Stock itself.
        self.stocks = OrderedDict({s.ticker: s for s in stocks})

    def add_stock(self, *stocks: stock):
        """Adds Stocks to the Portfolio only if the do not already exist.

        Args:
            *stocks (Stock): A Stock and its associated data
        """
        # Only add the Stocks that are not already in the Portfolio.

        if isinstance(stocks[0], stock):
            new_stocks = set(stocks).difference(set(self.stocks.values()))
            to_add = {s.ticker: s for s in new_stocks}
            self.stocks.update(to_add)
        # TODO Write function to collect data for new stocks
        if isinstance(stocks[0], str):
            new_stocks = set(stocks).difference(set(self.stocks.keys()))
            to_add = {s.ticker: s for s in new_stocks}
            self.stocks.update(to_add)

    def remove_stock(self, *stocks: stock):
        """Removes Stocks from the Portfolio only if they already exist.

        Args:
            *stocks (Stock): a Stock and its associated data
        """
        if isinstance(stocks[0], stock):
            # Only remove the Stocks that exist in the Portfolio.
            existing = set(stocks).intersection(set(self.stocks.values()))
            for s in existing:
                del self.stocks[s.ticker]

        if isinstance(stocks[0], str):
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

    def preview(self, anon=False):
        """Displays a table that contains each Stock, referred to by
        ticker (or pseudonym), the start and end dates of the data, and the
        number of shares owned of each Stock.

        Args:
            anon (bool):

        Returns:
            pandas DataFrame with Stock ticker, number of shares, start and end
            dates
        """

        def assign_label(stock_to_label):
            """Helper method for preview(). Determine the anonymity state of
            the Stock and assign the appropriate label.

            Returns:
                Stock's pseudonym if its anonymity state is True. Otherwise,
                return its ticker.
            """
            is_anonymous, pseudonym = stock_to_label.anonymous[self]
            return pseudonym if is_anonymous else stock_to_label.ticker

        # TODO Fix - if already anonymous, don't deanonymize
        # If preview is to be anonymous, make sure the Stocks are anonymized.
        if anon:
            self.anonymize()
        else:
            self.reveal()
        # List to store number of shares and start/end dates for all Stocks.
        info = []
        # List to store either tickers or pseudonyms for the table.
        index = []
        # For each Stock, determine assign the appropriate label and collect
        # the information to be assigned in the DataFrame.
        for s in self.stocks.values():
            if self in s.portfolios:
                label = assign_label(s)
                info.append([s.num_shares[self],
                             s.start_date[self],
                             s.end_date[self]])
                index.append(label)
        columns = ['Number of Shares', 'Start', 'End']
        return pd.DataFrame(data=info, columns=columns, index=index)

    def total_shares(self):
        """Calculate the total number of shares owned for all Stocks.

        Returns:
            Total number of Stock shares owned in the Portfolio
        """
        return sum([n.num_shares[self] for n in self.stocks.values()])

    def anonymize(self):
        """Anonymize all Stocks in the Portfolio by setting the bool anonymous
        attribute to True. The ticker symbol is preserved, but is hidden when
        Stock.anonymous is True.
        """

        def generate_pseudonym():
            """Generate a random integer between 0-1000 using
            numpy.random.permutation(1000)[0]. Prepend this with 'S-' to
            complete the pseudonym.

            Returns:
                Pseudonym of the form 'S-xxx' where xxx is a randomly generated
                integer between 0 and 999.
            """
            return 'S-' + str(np.random.permutation(1000)[0])

        # Create a set of existing pseudonyms for all Stocks.
        pseudos = set([pseudonym.anonymous[self][1] for pseudonym in
                       self.stocks.values()])
        # For each Stock in the Portfolio...
        for stock_data in self.stocks.values():
            # ...get the pseudonym for the Stock.
            pseudonym = stock_data.anonymous[self][1]
            # Until the pseudonym is unique amongst the existing pseudonyms...
            while pseudonym in pseudos:
                # ...generate another pseudonym.
                pseudonym = generate_pseudonym()
            # Assign this unique pseudonym to the Stock.
            stock_data.anonymous[self][1] = pseudonym
            # Assign the Stock's anonymity state to True.
            stock_data.anonymous[self][0] = True

    def reveal(self):
        """ Reveal the ticker symbols of all Stocks in the Portfolio by setting
        each Stock's anonymity state to False.
        """
        for s in self.stocks.values():
            s.anonymous[self][0] = False

    def get_data_slice(self, attribute: str, dated=True, as_dict=False):
        if dated:
            if as_dict:
                return {t: {s['date']: s[attribute] for s in data.price_data}
                        for t, data in self.stocks.items()}
            else:
                return [(t, [(s['date'], s[attribute])
                        for s in data.price_data])
                        for t, data in self.stocks.items()]
        else:
            if as_dict:
                return {t: [s[attribute] for s in data.price_data]
                        for t, data in self.stocks.items()}
            else:
                return [(t, [s[attribute] for s in data.price_data])
                        for t, data in self.stocks.items()]

