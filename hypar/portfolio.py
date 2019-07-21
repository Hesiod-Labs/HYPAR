<<<<<<< HEAD
import bisect
from dataclasses import dataclass, field
import datetime
import itertools
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
=======
from hypar.stock import Stock as stock
import pandas as pd
import numpy as np
from collections import OrderedDict
>>>>>>> 6f35e43c5e68e292d93c56847790b15dbbedc0b9

import stock

<<<<<<< HEAD

@dataclass(init=False, order=True)
class Portfolio(object):
=======
class Portfolio:
>>>>>>> 6f35e43c5e68e292d93c56847790b15dbbedc0b9
    """A collection of Stocks. Serves the purpose of collectively analyzing how
    a group of Stocks performs together over a duration of time. Analysis and
    group operations can be performed on a Portfolio as opposed to having to
    apply the operation to each Stock separately.

    Attributes:
        *stocks (dict[str, Stock]): Stocks belonging to the Portfolio. The key
            of each Stock is its ticker and the value is the Stock itself.
    """
<<<<<<< HEAD
    sort_index: datetime.datetime = field(init=False, repr=False)
    stocks: Dict[str, stock.Stock] = field(default_factory=dict)
    segments: List[stock.StockSegment] = field(default_factory=list)
    partition_dates: List[List[datetime.datetime]] = field(default_factory=list)
    partitions: Dict[Tuple[datetime.datetime],
                     List[stock.StockSegment]] = field(default_factory=dict)

    def __init__(self, *args, **kwargs):
        """Creates a Portfolio containing Stocks. Adds all Stocks to a list,
        aggregates all StockSegments to a single StockSegment list,
        and determines the partition dates that will determine how the
        Portfolio is partitioned.

        Arguments:
            *args: Stocks
            **kwargs: Any attribute meant to describe the Portfolio.
        """
        self.stocks = {s.ticker: s for s in args}
        self.segments = [se for s in self.stocks.values() for se in s.segments]
        self.segments.sort()
        self.partition_dates = self.find_partition_dates()
        self.partitions = self.partition()
        self.start = stock.first_start(self.segments)
        self.end = stock.last_end(self.segments)
        self.__dict__.update(kwargs)

    def __repr__(self):
        tickers = [t for t in self.stocks.keys()]
        return f'{self.__class__.__name__}(stocks={tickers}, ' \
            f'start={self.start:%Y-%m-%d}, end={self.end:%Y-%m-%d})'

    def find_partition_dates(self):
        """Determines the start and end dates that partitions the Portfolio
        based on its holdings. In the simplest case, there is a single
        start-end date pair. This occurs when all holdings are held once
        and continuously. Otherwise, more than one partition date pair exists
        that signifies when the Portfolio's holdings change.
        """
        # Create a start date set that will be used as primary condition for
        # range setting, and to eliminate duplicates.
        starts_set = set([s.start for s in self.segments])
        # Create an end date set to eliminate duplicates.
        ends_set = set([s.end for s in self.segments])
        # Create a list of dates to iterate through to generate date ranges.
        dates = list(starts_set)
        dates.extend(list(ends_set))
        dates.sort()
        # If either condition is satisfied, the dates are added as a range:
        # 1. Date is a start date and is not the same as the next date.
        # 2. Two consecutive dates are both end dates.
        return [[d, dates[i + 1]] for i, d in enumerate(dates)
                if (d in starts_set and d != dates[i + 1])
                or (i + 2 <= len(dates) and d in ends_set
                    and dates[i + 1] in ends_set)]

    def partition(self):
        """Partitions the Portfolio in accordance with its partition dates.
        In the simplest case, there is one partition. That is, when all
        holdings are held once and continuously. Otherwise, each partition
        signifies a change in holdings.

        Creates an empty dictionary to store the partitions such that each
        partition date pair tuple is the key and the StockSegments owned during
        that time are the values as a list.
=======

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
>>>>>>> 6f35e43c5e68e292d93c56847790b15dbbedc0b9
        """
        partitions = dict()
        for p_date in self.partition_dates:
            for seg in self.segments:
                if seg.start <= p_date[0] and seg.end >= p_date[1]:
                    if tuple(p_date) in set(partitions.keys()):
                        partitions[tuple(p_date)].append(seg)
                    else:
                        partitions[tuple(p_date)] = [seg]
        return partitions

    # TODO Replace with duck typing try-except
    def add(self, *args):
        new_stocks = [st for st in args if hasattr(st, 'segments')
                      and st.ticker not in self.stocks.keys()]
        segs = [seg for seg in args if not hasattr(seg, 'segments')
                and seg not in self.segments]
        segs.extend([s for st in new_stocks for s in st.segments if s not in
                     segs])
        segs.sort()

        for st in new_stocks:
            self.stocks[st.ticker] = st
        for s in segs:
            if s.ticker in self.stocks.keys():
                bisect.insort_left(self.stocks[s.ticker].segments, s)
            else:
                new_stock = stock.Stock(s)
                bisect.insort_left(self.stocks, new_stock)

        self.segments, self.start, self.end = stock.update(self.segments, segs)
        self.partition_dates = self.find_partition_dates()
        self.partitions = self.partition()

    def remove(self, *args):
        st_exist = [st for st in args if isinstance(st, stock.Stock)
                    and st in self.stocks.values()]
        se_exist = [seg for seg in args if isinstance(seg, stock.StockSegment)
                    and seg in self.segments]
        se_exist.extend([st.segments for st in st_exist])
        se_exist.sort()
        for s in st_exist:
            del self.stocks[s.ticker]
        self.segments = [s for s in self.segments if s not in se_exist]
        discard, self.start, self.end = stock.update(self.segments, [])

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
            s.anonymous = True

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

