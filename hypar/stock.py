from dataclasses import dataclass, field
from collections import deque
import datetime
import itertools
from typing import List, Dict, Any, Tuple, Set
SegmentID = str

# TODO
#   1. Add docstrings to all functions
#   2. Double check existing docstring is accurate
#   3. Add data attribute to Stock


def sort_by_start(element):
    """Sorting tool used to sort data class Stock and StockSegments by start
    date.

    Args:
        element: Segment or Stock

    Returns:
        datetime.datetime start date of the Segment or Stock.
    """
    return element.start


def sort_by_end(element):
    """Sorting tool used to sort data class Stock and StockSegments by end
        date.

        Args:
            element: Segment or Stock

        Returns:
            datetime.datetime end date of the Segment or Stock.
        """
    return element.end


def first_start(elements: Dict):
    """Sorts through all StockSegments or Stocks to find the earliest start
    date.

    Args:
        elements: Either Stock.segments or Portfolio.stocks Dict.

    Returns:
        Earliest datetime.datetime start date of a collection of either
        StockSegments or Stocks.
    """
    return sorted(list(elements.values()), key=sort_by_start)[0].start


def last_end(elements: Dict):
    """Sorts through all StockSegments or Stocks to find the latest end date.

    Args:
        elements: Either Stock.segments or Portfolio.stocks Dict.

    Returns:
        Latest datetime.datetime end date of a collection of either
        StockSegments or Stocks.
    """
    return sorted(list(elements.values()), key=sort_by_end)[-1].end


_new_id = itertools.count()
_free_ids = set()


@dataclass(order=True)
class Segment(object):
    """Usually a portion of an entire holding of a Stock, but could also be
    equivalent to the Stock itself if held continuously over the entire
    duration of the Stock's existence.

    Includes such properties as the number of shares owned and start and end
    dates of when the Segment is owned. Distinction of Segment(s) and
    StockData is necessary when dealing with a multi-Portfolio environment in
    which the number of shares and dates vary between one or more Portfolios.
    In this way, each Segment in one or more Portfolios can have
    different number of shares and dates.

    Key-referenced by its unique segment_id of the form <ticker>-123 where
    123 is uniquely assigned to that Segment. This is used exclusively
    for internal algorithmic efficiency when searching for a Segment.

    Attributes:
        sort_index (datetime.datetime): Used to compare by start date.
        ticker (str): Ticker symbol of the Stock.
        num_shares (int): Number of shares owned.
        start (datetime.datetime): Starting date.
        end (datetime.datetime): Ending date.
        anonymous (bool): True if the Segment is to be referred to by its
            pseudonym, and otherwise implies the Segment should be referred
            to by its ticker symbol.
        pseudonym (str): "S-XXX" where "XXX" is a unique integer generated at
            the time of Portfolio creation. Used in place of the ticker when the
            Segment is supposed to be anonymous.
        segment_id (str): "<ticker>-XXX" where "XXX" is a unique integer
            generated at the time of Stock creation. Used to uniquely and
            efficiently identify a Segment when searching through a
            Stock.segments or Portfolio.stocks Dicts.
    """
    sort_index: datetime.datetime = field(init=False, repr=False)
    ticker: str
    start: datetime.datetime
    end: datetime.datetime
    num_shares: int = 1
    anonymous: bool = field(default=False, repr=False)
    pseudonym: str = None
    segment_id: str = None

    def __post_init__(self):
        self.sort_index = self.start
        self.ticker = self.ticker.upper()

    def __repr__(self):
        return f'{self.__class__.__name__}(ticker={self.ticker}, ' \
            f'segment_id={self.segment_id}, pseudonym={self.pseudonym}, ' \
            f'start={self.start:%Y-%m-%d}, end={self.end:%Y-%m-%d})'


# TODO(Ryan) Specify type hints in more detail -- refer to PEP 483 and 484:
# https://www.python.org/dev/peps/pep-0483/#notational-conventions
# https://www.python.org/dev/peps/pep-0484/
@dataclass
class StockData(object):
    """Data about a Stock that is shared among all Segment(s) of a Stock.

    Collection of data that is parsed among all Segment(s) that, together,
    signifies the Stock activity during the date ranges in which it is owned.
    There may be regions of data that are not accessed if no Segment
    exists within that region of time.

    Attributes:
        ticker (str): Ticker symbol of the Stock.
        interday_pricing (List[Dict[str, Any]]): Daily adjusted and
        unadjusted price and volume information.
        balance_sheet (Dict[str, Any]): Balance sheet information of the most
            recent available quarter.
        book (Dict[str, Any]): Book data.
        cash_flow (Dict[str, Any]): Cash flow information of the most recent
            available quarter.
        company (Dict[str, Any]): Company information, such as the website,
            description, tags, and CEO.
        earnings (Dict[str, Any]): Earnings data for a given company,
            including the actual EPS, consensus, and fiscal period. Earnings are
            available for the most recent four quarters.
        estimate (Dict[str, Any]): Latest consensus estimate for the next
            fiscal period.
        income_statement (Dict[str, Any]): Income statement information from
            the most recent available quarter.
        intraday_pricing (Dict[str, Any]): Intraday trading information in
            one-minute intervals.
        ipo_today (Dict[str, List]): IPOs occurring today.
        ipo_upcoming (Dict[str, List]): IPOs in the near future.
        key_stats (Dict[str, Any]): Various summary data.
        price_target (Dict[str, Any]): Latest average, high, and low analyst
            price target.
    """
    ticker: str
    interday_pricing: List[Dict[str, Any]] = field(default_factory=list)
    balance_sheet: Dict[str, Any] = field(default_factory=dict)
    book: Dict[str, float] = field(default_factory=dict)
    cash_flow: Dict[str, Any] = field(default_factory=dict)
    company: Dict[str, Any] = field(default_factory=dict)
    earnings: Dict[str, Any] = field(default_factory=dict)
    # TODO Add to docstring
    dividends: List[Dict[str, Any]] = field(default_factory=list)
    # TODO Add to docstring
    news: List[Dict[str, Any]] = field(default_factory=list)
    # TODO Add to docstring
    sector_performance: List[Dict[str, Any]] = field(default_factory=list)
    # TODO Add to docstring
    peers: List[str] = field(default_factory=list)
    estimate: Dict[str, Any] = field(default_factory=dict)
    income_statement: Dict[str, Any] = field(default_factory=dict)
    intraday_pricing: List[Dict[str, Any]] = field(default_factory=list)
    ipo_today: Dict[str, List] = field(default_factory=dict)
    ipo_upcoming: Dict[str, List] = field(default_factory=dict)
    key_stats: Dict[str, Any] = field(default_factory=dict)
    price_target: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.ticker = self.ticker.upper()


@dataclass(init=False, order=True)
class Stock(object):
    """A Dict of one or more StockSegment(s) that define the Stock.

    In the simplest case, a Stock is one StockSegment. But if the Stock is not
    held continuously over the duration of the Portfolio's time frame, more than
    one StockSegment comprises the Stock.

    Also has the same attributes as a StockSegment, such as start date and
    end date. A Stock's pseudonym is modified such that if a Stock owns
    multiple StockSegments, it is appended with an "x". The pseudonym is not
    generated until Portfolio creation to ensure uniqueness.

    Attributes:
        ticker (str): Ticker symbol.
        segments (Dict[SegmentID, Segment]): One or more
            StockSegments that reference the same StockData. If there is only
            one continuous holding of a StockSegment, then the Stock and the
            single StockSegment are equivalent. If listed and sorted,
            StockSegments are sorted according to start date by default.
        segment_ids (Set[SegmentID]): Unique string identifiers
            used to efficiently search for a StockSegment.
        start (datetime.datetime): The earliest of the Stock's StockSegments'
            start dates.
        end (datetime.datetime): The latest of the Stock's StockSegments' end
            dates.
    """
    sort_index: datetime.datetime = field(init=False, repr=False)

    def __init__(self, *segments, **kwargs):
        """Creates a Stock from one or more StockSegments.

        Arguments:
            *segments: One or more StockSegments.
            **kwargs: Any attribute that is intended to describe a Stock.
        """
        self.ticker = list(segments)[0].ticker
        self.pseudonym = ''
        self.anonymous = False
        self.segments = self.finalize_segments(segments)
        self.segment_ids = set([s for s in self.segments.keys()])
        self.start = first_start(self.segments)
        self.sort_index = self.start
        self.end = last_end(self.segments)
        self.__dict__.update(kwargs)

    def __repr__(self):
        return f'{self.__class__.__name__}(ticker={self.ticker}, ' \
            f'pseudonym={self.pseudonym}, start={self.start:%Y-%m-%d}, ' \
            f'end={self.end:%Y-%m-%d})'

    # TODO Copy parts from finalize_segments docstring
    @staticmethod
    def assign_seg_id(seg: Segment):
        """
        """
        if _free_ids:
            seg.segment_id = f'{seg.ticker}-{_free_ids.pop()}'
        else:
            seg.segment_id = f'{seg.ticker}-{next(_new_id)}'

    def finalize_segments(self, segments: Tuple):
        """Generates Segment segment_id given a tuple of StockSegments.

        Used when creating a Stock to ensure segment_ids of StockSegments are
        unique. Format of a segment_id is <ticker>-123 where 123 is the generated
        component from an itertools.count() generator.

        A preliminary check is made to see if the set containing any previous
        created, but no longer active, segment_ids is is empty. If it is not
        empty, a segment_id is popped and used, rather than counting up from the
        itertools.counter(). This prevents unnecessarily large numerical
        components of the segment_id.

        Arguments:
            segments: Tuple of StockSegments to assign segment_ids.

        Returns:
            Dict that is Stock.segments and formatted as
            Dict[Segment.segment_id, Segment].
        """
        for seg in segments:
            if not seg.segment_id:
                self.assign_seg_id(seg)
        return {s.segment_id: s for s in segments}

    def get_segment(self, segment):
        if segment.segment_id in self.segment_ids:
            return self.segments[segment.segment_id]
        else:
            print(f'{segment.segment_id} does not exist.')

    def add_segment(self, *segments: Segment):
        """Add one or more StockSegments to an existing Stock. Begin by
        checking that all StockSegments to be added do not already exist.
        After adding all StockSegments, update the start and end dates if any of
        the new StockSegments have an earlier start date or later end date
        than the existing start and end date of the Stock.

        Arguments:
            *segments: One or more StockSegments to be added to the Stock.
        """
        for seg in segments:
            if not seg.segment_id or seg.segment_id in self.segments:
                self.assign_seg_id(seg)
                self.update_stock_dates(seg)
                self.segments[seg.segment_id] = seg
        self.update_stock_pseudonym()

    def remove_segment(self, *segments: Segment):
        """Remove one or more StockSegments from the Stock. First checks that
        any Segment to be removed exists in the Stock.

        Arguments:
            *segments: One or more StockSegments to remove.
        """
        for seg in segments:
            if seg.segment_id in self.segment_ids:
                seg_del = seg
                _free_ids.add(seg_del.segment_id)
                del self.segments[seg.segment_id]
                self.update_stock_dates(seg_del, add=False)
        self.update_stock_pseudonym()

    def update_stock_dates(self, segment, add=True):
        if segment.start <= self.start:
            self.start = segment.start if add else first_start(self.segments)
        if segment.end >= self.end:
            self.end = segment.end if add else last_end(self.segments)

    def update_stock_pseudonym(self):
        try:
            if len(self.segments) <= 1 and self.pseudonym.endswith('x'):
                self.pseudonym = self.pseudonym[:-1]
            else:
                self.pseudonym = ''.join((self.pseudonym, 'x'))
        except AttributeError:
            print(f"{self.ticker} has no pseudonym.")
