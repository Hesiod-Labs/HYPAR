from dataclasses import dataclass
import itertools
import numpy as np
from typing import Dict, Tuple, Union

import stock

# TODO
#   1. Add docstring to all functions that don't have them
#   2. Double check existing docstring is accurate.
#   3. Test all functions.
#   4. Push to GitHub
#   4. Mixins for shared functions, like sorting, and maybe adding/removing
#   5. Switch from to EAFP

_free_pseudos = set()
_new_pseudo = itertools.count()


@dataclass(init=False)
class Portfolio(object):
    """A collection of Stocks. Serves the purpose of collectively analyzing how
    a group of Stocks performs together over a duration of time. Analysis and
    group operations can be performed on a Portfolio as opposed to having to
    apply the operation to each Stock and Segment(s) separately.

    Attributes:
        stocks (Dict[str, Stock]): Each Stock may contain more than one
            Segment. Each Segment corresponds to a partition date in
            which a unique sub-Portfolio exists.
    """
    def __init__(self, *stocks, **kwargs):
        """Creates a Portfolio containing Stocks. Adds all Stocks to a list,
        aggregates all StockSegments to a single Segment list,
        and determines the partition dates that will determine how the
        Portfolio is partitioned.

        Arguments:
            *args: Stocks
            **kwargs: Any attribute meant to describe the Portfolio.
        """
        self.stocks = self.finalize_stocks(stocks)
        self.stock_ids = set(list(self.stocks.keys()))
        self.partition_dates = self.find_partition_dates()
        self.start = stock.first_start(self.stocks)
        self.end = stock.last_end(self.stocks)
        self.is_watchlist = False
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
        starts_set = set([seg.start for s in self.stocks.values() for seg in
                          s.segments.values()])
        # Create an end date set to eliminate duplicates.
        ends_set = set([seg.end for s in self.stocks.values() for seg in
                        s.segments.values()])
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

    @staticmethod
    def assign_pseudo(element: Union[stock.Stock, stock.Segment]):
        pseudo = _free_pseudos.pop() if _free_pseudos else next(_new_pseudo)
        if hasattr(element, 'segment_id'):
            element.pseudonym = f'S-{pseudo}'
        elif len(element.segments) > 1:
            element.pseudonym = f'S-{pseudo}x'
        else:
            element.pseudonym = f'S-{pseudo}'

    def finalize_stocks(self, stocks):
        for s in list(stocks):
            for seg in s.segments.values():
                if not seg.pseudonym:
                    self.assign_pseudo(seg)
            self.assign_pseudo(s)
        return {s.ticker: s for s in stocks}

    def get_stock(self, stk: Union[stock.Stock, str]):
        if isinstance(stk, stock.Stock) and stk.ticker in self.stock_ids:
            return self.stocks[stk.ticker]
        elif isinstance(stk, str) and stk in self.stock_ids:
            return self.stocks[stk]
        else:
            print('Stock is not present in the Portfolio.')

    def get_segment(self, seg: Union[stock.Segment, str]):
        if isinstance(seg, stock.Segment) and seg.ticker in self.stock_ids:
            return self.stocks[seg.ticker].get_segment(seg)
        elif isinstance(seg, str) and seg in self.stock_ids:
            return self.stocks[seg].segments
        else:
            print('Segment is not present in the Portfolio.')

    # TODO Left off here (7/14/19)
    # TODO Generate pseudonyms
    def add_stocks(self, *stk: stock.Stock):
        for s in stk:
            if s.ticker not in self.stock_ids:
                self.stock_ids.add(s.ticker)
                if s.start < self.start:
                    self.start = s.start
                if s.end > self.end:
                    self.end = s.end
                self.stocks[s.ticker] = stk
            else:
                print('Stock is already in the Portfolio.')
        self.partition_dates = self.find_partition_dates()

    # TODO Generate pseudonyms
    def add_segment(self, seg: stock.Segment):
        if seg.ticker not in self.stock_ids:
            new_stock = stock.Stock(seg)
            if new_stock.start < self.start:
                self.start = new_stock.start
            if new_stock.end > self.end:
                self.end = new_stock.end

    # TODO Split up into remove_stock and remove_segment
    def remove(self, *args):
        st_exist = [st for st in args if isinstance(st, stock.Stock)
                    and st in self.stocks.values()]
        se_exist = [seg for seg in args if isinstance(seg, stock.Segment)
                    and seg in self.segments]
        se_exist.extend([st.segments for st in st_exist])
        se_exist.sort()
        for s in st_exist:
            del self.stocks[s.ticker]
        self.segments = [s for s in self.segments if s not in se_exist]
        discard, self.start, self.end = stock.update(self.segments, [])

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
            for seg in s.segments.values:
                seg.anonymous = False
            s.anonymous = False

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
