from dataclasses import dataclass, field
import datetime
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple

from stock import Stock, StockSegment


@dataclass(init=False)
class Portfolio(object):
    """A collection of Stocks. Serves the purpose of collectively analyzing how
    a group of Stocks performs together over a duration of time. Analysis and
    group operations can be performed on a Portfolio as opposed to having to
    apply the operation to each Stock and StockSegment(s) separately.

    Attributes:
        stocks (List[Stock]): Each Stock may contain more than one
        StockSegment. Each StockSegment corresponds to a partition date in
        which a unique sub-Portfolio exists.
    """
    stocks: List[Stock] = field(default_factory=list)
    segments: List[StockSegment] = field(default_factory=list)
    partition_dates: List[List[datetime.datetime]] = field(default_factory=list)
    partitions: Dict[Tuple[datetime.datetime],
                     List[StockSegment]] = field(default_factory=dict)

    def __init__(self, *args, **kwargs):
        """Creates a Portfolio containing Stocks. Adds all Stocks to a list,
        aggregates all StockSegments to a single StockSegment list,
        and determines the partition dates that will determine how the
        Portfolio is partitioned.

        Arguments:
            *args: Stocks
            **kwargs: Any attribute meant to describe the Portfolio.
        """
        self.stocks = list(args)
        self.segments = [seg for s in self.stocks for seg in s.segments]
        self.partition_dates = self.get_partition_dates()
        self.partitions = self.partition()
        self.__dict__.update(kwargs)

    def __repr__(self):
        tickers = [t.ticker for t in self.stocks]
        start = sorted([d.start_date for s in self.stocks for d in s.segments])
        end = sorted([d.end_date for s in self.stocks for d in s.segments])
        return f'{self.__class__.__name__}(stocks={tickers}, ' \
            f'start={start[0]:%Y-%m-%d}, end={end[-1]:%Y-%m-%d})'

    # TODO Add docstring
    def get_partition_dates(self):
        """Determines the start and end dates that partitions the Portfolio
        based on its holdings. In the simplest case, there is a single
        start-end date pair. This occurs when all holdings are held once
        and continuously. Otherwise, more than one partition date pair exists
        that signifies when the Portfolio's holdings change.
        """
        # Create a start date set that will be used as primary condition for
        # range setting, and to eliminate duplicates.
        starts_set = set([s.start_date for s in self.segments])
        # Create an end date set to eliminate duplicates.
        ends_set = set([s.end_date for s in self.segments])
        # Create a list of dates to iterate through to generate date ranges.
        dates = list(starts_set) + list(ends_set)
        # Sort so that the earliest dates are towards the beginning.
        dates = sorted(dates)
        # If either condition is satisfied, the dates are added as a range:
        # 1. Date is a start date and is not the same as the next date.
        # 2. Two consecutive dates are both end dates.
        return [[d, dates[i + 1]] for i, d in enumerate(dates)
                if (d in starts_set and d != dates[i + 1])
                or (i + 2 <= len(dates) and d not in starts_set
                    and dates[i + 1] not in starts_set)]

    def partition(self):
        """Partitions the Portfolio in accordance with its partition dates.
        In the simplest case, there is one partition. That is, when all
        holdings are held once and continuously. Otherwise, each partition
        signifies a change in holdings.

        Creates an empty dictionary to store the partitions such that each
        partition date pair tuple is the key and the StockSegments owned during
        that time are the values as a list.
        """
        partitions = dict()
        for p_date in self.partition_dates:
            for seg in self.segments:
                if seg.start_date <= p_date[0] and seg.end_date >= p_date[1]:
                    if tuple(p_date) in set(partitions.keys()):
                        partitions[tuple(p_date)].append(seg)
                    else:
                        partitions[tuple(p_date)] = [seg]
        return partitions

    # TODO Update Portfolio.segments
    def add_stock(self, *stocks: Stock):
        existing = set(self.stocks)
        for stock in stocks:
            if stock not in existing:
                self.stocks.append(stock)
        self.partition_dates = self.get_partition_dates()
        self.partitions = self.partition()

    # TODO Update Portfolio.segments
    def remove_stock(self, *stocks: Stock):
        existing = set(self.stocks)
        for stock in stocks:
            if stock in existing:
                self.stocks.remove(stock)

    # TODO Deprecated - needs rewritten (7/6/19)
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

    # TODO Deprecated - needs rewritten (7/6/19)
    def total_shares(self):
        """Calculate the total number of shares owned for all Stocks.

        Returns:
            Total number of Stock shares owned in the Portfolio
        """
        return sum([n.num_shares[self] for n in self.stocks.values()])

    # TODO Deprecated - needs rewritten (7/6/19)
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

    # TODO Deprecated - needs rewritten (7/6/19)
    def reveal(self):
        """ Reveal the ticker symbols of all Stocks in the Portfolio by setting
        each Stock's anonymity state to False.
        """
        for s in self.stocks.values():
            s.anonymous[self][0] = False

    # TODO Deprecated - needs rewritten (7/6/19)
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
